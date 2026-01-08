"""
YOKATLAS MCP Server - Turkish Higher Education Atlas API

This module provides an MCP server for accessing YOKATLAS data,
including bachelor's and associate degree program information.
"""

import logging
from typing import Literal, Optional, List, Any

from pydantic import Field
from fastmcp import FastMCP

# Import yokatlas-py v0.5.4+ API
from yokatlas_py import (
    search_lisans_programs,
    search_onlisans_programs,
    YOKATLASLisansAtlasi,
    YOKATLASOnlisansAtlasi
)

# Public API exports
__all__ = ["app", "main"]

# Configure logging
logger = logging.getLogger(__name__)

# Create a FastMCP server instance
app = FastMCP(
    name="YOKATLAS API Server",
    instructions="MCP server for Turkish Higher Education Atlas (YOKATLAS). Provides access to university program data including bachelor's and associate degree programs with search and detailed statistics."
)


# =============================================================================
# Helper Functions (DRY - Don't Repeat Yourself)
# =============================================================================

def _build_search_params(
    university: Optional[str],
    program: Optional[str],
    city: Optional[str],
    university_type: str,
    fee_type: str,
    education_type: str,
    availability: str,
    results_limit: int,
    score_type: Optional[str] = None
) -> dict:
    """
    Build search parameters dictionary for YOKATLAS API.

    Args:
        university: University name filter
        program: Program name filter
        city: City filter
        university_type: University type filter
        fee_type: Fee type filter
        education_type: Education type filter
        availability: Availability filter
        results_limit: Maximum results to return
        score_type: Score type filter (only for bachelor programs)

    Returns:
        Dictionary of search parameters for yokatlas-py API
    """
    params: dict[str, Any] = {}

    if university:
        params['universite'] = university
    if program:
        params['program'] = program
    if city:
        params['sehir'] = city
    if score_type:
        params['puan_turu'] = score_type.lower()
    if university_type:
        params['universite_turu'] = university_type
    if fee_type:
        params['ucret'] = fee_type
    if education_type:
        params['ogretim_turu'] = education_type
    if availability:
        params['doluluk'] = availability
    if results_limit:
        params['length'] = results_limit

    return params


def _execute_search(
    search_func: callable,
    params: dict,
    program_type: str,
    search_context: dict
) -> dict:
    """
    Execute a search and format the results.

    Args:
        search_func: The search function to call (search_lisans_programs or search_onlisans_programs)
        params: Search parameters dictionary
        program_type: Type of program ('bachelor' or 'associate_degree')
        search_context: Context info for error reporting (university, program, city)

    Returns:
        Formatted search results dictionary
    """
    try:
        results = search_func(params, smart_search=True)

        # Handle error response from API
        if isinstance(results, dict) and 'error' in results:
            logger.warning(f"API returned error for {program_type} search: {results.get('error')}")
            return results

        # Format successful results
        response = {
            "programs": results if isinstance(results, list) else [],
            "total_found": len(results) if isinstance(results, list) else 0,
            "search_method": "smart_search_v0.5.4",
            "fuzzy_matching": True
        }

        if program_type == "associate_degree":
            response["program_type"] = "associate_degree"

        return response

    except ValueError as e:
        logger.error(f"Invalid parameter in {program_type} search: {e}")
        return {
            "error": "Invalid search parameter",
            "details": str(e),
            "search_method": "smart_search_v0.5.4",
            "parameters_used": search_context
        }
    except ConnectionError as e:
        logger.error(f"Connection error in {program_type} search: {e}")
        return {
            "error": "Connection error to YOKATLAS",
            "details": str(e),
            "search_method": "smart_search_v0.5.4",
            "parameters_used": search_context
        }
    except Exception as e:
        logger.exception(f"Unexpected error in {program_type} search")
        return {
            "error": "Internal error",
            "details": str(e),
            "search_method": "smart_search_v0.5.4",
            "parameters_used": search_context
        }


async def _fetch_atlas_details(
    atlas_class: type,
    yop_kodu: str,
    year: int,
    program_type: str
) -> dict:
    """
    Fetch detailed atlas information for a program.

    Args:
        atlas_class: Atlas class to use (YOKATLASLisansAtlasi or YOKATLASOnlisansAtlasi)
        yop_kodu: Program YOP code
        year: Data year
        program_type: Type of program for logging

    Returns:
        Atlas details dictionary or error dictionary
    """
    try:
        atlas = atlas_class({'program_id': yop_kodu, 'year': year})
        result = await atlas.fetch_all_details()
        return result
    except ValueError as e:
        logger.error(f"Invalid parameter for {program_type} atlas: {e}")
        return {"error": "Invalid parameter", "details": str(e), "program_id": yop_kodu, "year": year}
    except ConnectionError as e:
        logger.error(f"Connection error fetching {program_type} atlas: {e}")
        return {"error": "Connection error to YOKATLAS", "details": str(e), "program_id": yop_kodu, "year": year}
    except Exception as e:
        logger.exception(f"Unexpected error fetching {program_type} atlas details")
        return {"error": "Internal error", "details": str(e), "program_id": yop_kodu, "year": year}


# =============================================================================
# MCP Tools
# =============================================================================

@app.tool()
async def get_associate_degree_atlas_details(
    yop_kodu: str = Field(description="Program YÖP code (e.g., '120910060') - unique identifier for the associate degree program"),
    year: int = Field(description="Data year for statistics (e.g., 2025, 2024, 2023)", ge=2020, le=2030)
) -> dict:
    """
    Get comprehensive details for a specific associate degree program from YOKATLAS Atlas.

    Parameters:
    - yop_kodu (str): Program YÖP code (e.g., '120910060')
    - year (int): Data year (e.g., 2025, 2024, 2023)

    Returns detailed information including:
    - General program information and statistics
    - Quota, placement, and score data
    - Student demographics and distribution
    - Academic staff and facility information
    - Historical placement trends
    """
    return await _fetch_atlas_details(YOKATLASOnlisansAtlasi, yop_kodu, year, "associate_degree")


@app.tool()
async def get_bachelor_degree_atlas_details(
    yop_kodu: str = Field(description="Program YÖP code (e.g., '102210277') - unique identifier for the bachelor's degree program"),
    year: int = Field(description="Data year for statistics (e.g., 2025, 2024, 2023)", ge=2020, le=2030)
) -> dict:
    """
    Get comprehensive details for a specific bachelor's degree program from YOKATLAS Atlas.

    Parameters:
    - yop_kodu (str): Program YÖP code (e.g., '102210277')
    - year (int): Data year (e.g., 2025, 2024, 2023)

    Returns detailed information including:
    - General program information and statistics
    - Quota, placement, and score data
    - Student demographics and distribution
    - Academic staff and facility information
    - Historical placement trends
    """
    return await _fetch_atlas_details(YOKATLASLisansAtlasi, yop_kodu, year, "bachelor")


@app.tool()
def search_bachelor_degree_programs(
    university: Optional[str] = Field(default='', description="University name with fuzzy matching support (e.g., 'boğaziçi' → 'BOĞAZİÇİ ÜNİVERSİTESİ')"),
    program: Optional[str] = Field(default='', description="Program/department name with partial matching (e.g., 'bilgisayar' finds all computer programs)"),
    city: Optional[str] = Field(default='', description="City name where the university is located"),
    score_type: Literal['SAY', 'EA', 'SOZ', 'DIL'] = Field(default='SAY', description="Score type: SAY (Science), EA (Equal Weight), SOZ (Verbal), DIL (Language)"),
    university_type: Literal['', 'Devlet', 'Vakıf', 'KKTC', 'Yurt Dışı'] = Field(default='', description="University type: Devlet (State), Vakıf (Foundation), KKTC (TRNC), Yurt Dışı (International)"),
    fee_type: Literal['', 'Ücretsiz', 'Ücretli', 'İÖ-Ücretli', 'Burslu', '%50 İndirimli', '%25 İndirimli', 'AÖ-Ücretli', 'UÖ-Ücretli'] = Field(default='', description="Fee status: Ücretsiz (Free), Ücretli (Paid), İÖ-Ücretli (Evening-Paid), Burslu (Scholarship), İndirimli (Discounted), AÖ-Ücretli (Open Education-Paid), UÖ-Ücretli (Distance Learning-Paid)"),
    education_type: Literal['', 'Örgün', 'İkinci', 'Açıköğretim', 'Uzaktan'] = Field(default='', description="Education type: Örgün (Regular), İkinci (Evening), Açıköğretim (Open Education), Uzaktan (Distance Learning)"),
    availability: Literal['', 'Doldu', 'Doldu#', 'Dolmadı', 'Yeni'] = Field(default='', description="Program availability: Doldu (Filled), Doldu# (Filled with conditions), Dolmadı (Not filled), Yeni (New program)"),
    results_limit: int = Field(default=50, ge=1, le=500, description="Maximum number of results to return")
) -> dict:
    """
    Search for bachelor's degree programs with smart fuzzy matching and user-friendly parameters.

    Smart Features:
    - Fuzzy university name matching (e.g., "boğaziçi" → "BOĞAZİÇİ ÜNİVERSİTESİ")
    - Partial program name matching (e.g., "bilgisayar" finds all computer programs)
    - Intelligent parameter normalization
    - Type-safe validation

    Parameters:
    - university: University name (fuzzy matching supported)
    - program: Program/department name (partial matching supported)
    - city: City name
    - score_type: Score type (SAY, EA, SOZ, DIL)
    - university_type: Type of university (Devlet, Vakıf, etc.)
    - fee_type: Fee/scholarship information
    - education_type: Type of education (Örgün, İkinci, etc.)
    - results_limit: Maximum number of results to return
    """
    params = _build_search_params(
        university=university,
        program=program,
        city=city,
        university_type=university_type,
        fee_type=fee_type,
        education_type=education_type,
        availability=availability,
        results_limit=results_limit,
        score_type=score_type
    )

    search_context = {"university": university, "program": program, "city": city}
    return _execute_search(search_lisans_programs, params, "bachelor", search_context)


@app.tool()
def search_associate_degree_programs(
    university: Optional[str] = Field(default='', description="University name with fuzzy matching support (e.g., 'anadolu' → 'ANADOLU ÜNİVERSİTESİ')"),
    program: Optional[str] = Field(default='', description="Program name with partial matching (e.g., 'turizm' finds all tourism programs)"),
    city: Optional[str] = Field(default='', description="City name where the university is located"),
    university_type: Literal['', 'Devlet', 'Vakıf', 'KKTC', 'Yurt Dışı'] = Field(default='', description="University type: Devlet (State), Vakıf (Foundation), KKTC (TRNC), Yurt Dışı (International)"),
    fee_type: Literal['', 'Ücretsiz', 'Ücretli', 'İÖ-Ücretli', 'Burslu', '%50 İndirimli', '%25 İndirimli', 'AÖ-Ücretli', 'UÖ-Ücretli'] = Field(default='', description="Fee status: Ücretsiz (Free), Ücretli (Paid), İÖ-Ücretli (Evening-Paid), Burslu (Scholarship), İndirimli (Discounted), AÖ-Ücretli (Open Education-Paid), UÖ-Ücretli (Distance Learning-Paid)"),
    education_type: Literal['', 'Örgün', 'İkinci', 'Açıköğretim', 'Uzaktan'] = Field(default='', description="Education type: Örgün (Regular), İkinci (Evening), Açıköğretim (Open Education), Uzaktan (Distance Learning)"),
    availability: Literal['', 'Doldu', 'Doldu#', 'Dolmadı', 'Yeni'] = Field(default='', description="Program availability: Doldu (Filled), Doldu# (Filled with conditions), Dolmadı (Not filled), Yeni (New program)"),
    results_limit: int = Field(default=50, ge=1, le=500, description="Maximum number of results to return")
) -> dict:
    """
    Search for associate degree (önlisans) programs with smart fuzzy matching and user-friendly parameters.

    Smart Features:
    - Fuzzy university name matching (e.g., "anadolu" → "ANADOLU ÜNİVERSİTESİ")
    - Partial program name matching (e.g., "turizm" finds all tourism programs)
    - Intelligent parameter normalization
    - Type-safe validation

    Parameters:
    - university: University name (fuzzy matching supported)
    - program: Program/department name (partial matching supported)
    - city: City name
    - university_type: Type of university (Devlet, Vakıf, etc.)
    - fee_type: Fee/scholarship information
    - education_type: Type of education (Örgün, İkinci, etc.)
    - results_limit: Maximum number of results to return

    Note: Associate degree programs use TYT scores, not SAY/EA/SOZ/DIL like bachelor programs.
    """
    params = _build_search_params(
        university=university,
        program=program,
        city=city,
        university_type=university_type,
        fee_type=fee_type,
        education_type=education_type,
        availability=availability,
        results_limit=results_limit
    )

    search_context = {"university": university, "program": program, "city": city}
    return _execute_search(search_onlisans_programs, params, "associate_degree", search_context)


def main():
    """Main entry point for the YOKATLAS MCP server."""
    app.run()


if __name__ == "__main__":
    main()
