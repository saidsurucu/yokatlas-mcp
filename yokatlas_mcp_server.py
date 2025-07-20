import asyncio  # Required for async yokatlas_py functions
from typing import Literal

from fastmcp import FastMCP

# Import the new smart search functions (v0.4.3+)
try:
    from yokatlas_py import search_lisans_programs, search_onlisans_programs
    from yokatlas_py import YOKATLASLisansAtlasi, YOKATLASOnlisansAtlasi
    from yokatlas_py.models import SearchParams, ProgramInfo
    NEW_SMART_API = True
except ImportError:
    # Fallback to older API structure
    try:
        from yokatlas_py import YOKATLASLisansTercihSihirbazi, YOKATLASOnlisansTercihSihirbazi
        from yokatlas_py import YOKATLASLisansAtlasi, YOKATLASOnlisansAtlasi
        from yokatlas_py.models import SearchParams, ProgramInfo
        NEW_SMART_API = False
    except ImportError:
        # Final fallback to very old structure
        from yokatlas_py.lisansatlasi import YOKATLASLisansAtlasi
        from yokatlas_py.lisanstercihsihirbazi import YOKATLASLisansTercihSihirbazi
        from yokatlas_py.onlisansatlasi import YOKATLASOnlisansAtlasi
        from yokatlas_py.onlisanstercihsihirbazi import YOKATLASOnlisansTercihSihirbazi
        NEW_SMART_API = False

# Create a FastMCP server instance
mcp = FastMCP("YOKATLAS API Server")

# Tool for YOKATLAS Onlisans Atlasi
@mcp.tool()
async def get_associate_degree_atlas_details(yop_kodu: str, year: int) -> dict:
    """
    Get comprehensive details for a specific associate degree program from YOKATLAS Atlas.
    
    Parameters:
    - yop_kodu (str): Program YÖP code (e.g., '120910060')
    - year (int): Data year (e.g., 2024, 2023)
    
    Returns detailed information including:
    - General program information and statistics
    - Quota, placement, and score data
    - Student demographics and distribution
    - Academic staff and facility information
    - Historical placement trends
    """
    try:
        onlisans_atlasi = YOKATLASOnlisansAtlasi({'program_id': yop_kodu, 'year': year})
        result = await onlisans_atlasi.fetch_all_details()
        return result
    except Exception as e:
        # Log error or handle it as appropriate for your MCP server
        # For now, re-raising or returning an error structure
        print(f"Error in get_associate_degree_atlas_details: {e}")
        return {"error": str(e), "program_id": yop_kodu, "year": year}

# Tool for YOKATLAS Lisans Atlasi
@mcp.tool()
async def get_bachelor_degree_atlas_details(yop_kodu: str, year: int) -> dict:
    """
    Get comprehensive details for a specific bachelor's degree program from YOKATLAS Atlas.
    
    Parameters:
    - yop_kodu (str): Program YÖP code (e.g., '102210277')
    - year (int): Data year (e.g., 2024, 2023)
    
    Returns detailed information including:
    - General program information and statistics
    - Quota, placement, and score data
    - Student demographics and distribution
    - Academic staff and facility information
    - Historical placement trends
    """
    try:
        lisans_atlasi = YOKATLASLisansAtlasi({'program_id': yop_kodu, 'year': year})
        result = await lisans_atlasi.fetch_all_details()
        return result
    except Exception as e:
        print(f"Error in get_bachelor_degree_atlas_details: {e}")
        return {"error": str(e), "program_id": yop_kodu, "year": year}

# Tool for YOKATLAS Lisans Search with Smart Features
@mcp.tool()
def search_bachelor_degree_programs(
    # User-friendly parameters with fuzzy matching
    university: str = '',              # University name (supports fuzzy matching like "boğaziçi", "odtu")
    program: str = '',                 # Program name (supports partial matching like "bilgisayar", "mühendislik")
    city: str = '',                    # City name (like "istanbul", "ankara")
    score_type: Literal['SAY', 'EA', 'SOZ', 'DIL'] = 'SAY',  # Score type for bachelor programs
    university_type: Literal['', 'Devlet', 'Vakıf', 'KKTC', 'Yurt Dışı'] = '',  # University type
    fee_type: Literal['', 'Ücretsiz', 'Ücretli', 'İÖ-Ücretli', 'Burslu', '%50 İndirimli', '%25 İndirimli', 'AÖ-Ücretli', 'UÖ-Ücretli'] = '',  # Fee/scholarship type
    education_type: Literal['', 'Örgün', 'İkinci', 'Açıköğretim', 'Uzaktan'] = '',  # Education type
    availability: Literal['', 'Doldu', 'Doldu#', 'Dolmadı', 'Yeni'] = '',  # Program availability status
    results_limit: int = 50,           # Number of results to return (default: 50)
    # Legacy parameter support for backward compatibility
    uni_adi: str = '',
    program_adi: str = '',
    sehir: str = '',
    puan_turu: str = '',
    universite_turu: str = '',
    ucret_burs: str = '',
    ogretim_turu: str = '',
    length: int = 0
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
    try:
        if NEW_SMART_API:
            # Use new smart search functions (v0.4.3+)
            search_params = {}
            
            # Map user-friendly parameters to API parameters
            if university or uni_adi:
                search_params['uni_adi'] = university or uni_adi
            if program or program_adi:
                search_params['program_adi'] = program or program_adi
            if city or sehir:
                search_params['city'] = city or sehir
            if score_type or puan_turu:
                search_params['score_type'] = score_type or puan_turu
            if university_type or universite_turu:
                search_params['university_type'] = university_type or universite_turu
            if fee_type or ucret_burs:
                search_params['fee_type'] = fee_type or ucret_burs
            if education_type or ogretim_turu:
                search_params['education_type'] = education_type or ogretim_turu
            if results_limit or length:
                search_params['length'] = results_limit or length
                
            # Use smart search with fuzzy matching
            results = search_lisans_programs(search_params, smart_search=True)
            
            # Validate and format results
            validated_results = []
            for program_data in results:
                try:
                    program = ProgramInfo(**program_data)
                    validated_results.append(program.model_dump())
                except Exception:
                    # Include unvalidated data if validation fails
                    validated_results.append(program_data)
            
            return {
                "programs": validated_results,
                "total_found": len(validated_results),
                "search_method": "smart_search_v0.4.3",
                "fuzzy_matching": True
            }
            
        else:
            # Fallback to legacy API
            params = {
                'uni_adi': university or uni_adi,
                'program_adi': program or program_adi,
                'sehir_adi': city or sehir,
                'puan_turu': (score_type or puan_turu).lower() if (score_type or puan_turu) else 'say',
                'universite_turu': university_type or universite_turu,
                'ucret_burs': fee_type or ucret_burs,
                'ogretim_turu': education_type or ogretim_turu,
                'page': 1
            }
            
            # Remove empty parameters
            params = {k: v for k, v in params.items() if v}
            
            lisans_tercih = YOKATLASLisansTercihSihirbazi(params)
            result = lisans_tercih.search()
            
            return {
                "programs": result[:results_limit] if isinstance(result, list) else result,
                "total_found": len(result) if isinstance(result, list) else 0,
                "search_method": "legacy_api",
                "fuzzy_matching": False
            }
            
    except Exception as e:
        print(f"Error in search_bachelor_degree_programs: {e}")
        return {
            "error": str(e), 
            "search_method": "smart_search" if NEW_SMART_API else "legacy_api",
            "parameters_used": {
                "university": university or uni_adi,
                "program": program or program_adi,
                "city": city or sehir
            }
        }

# Tool for YOKATLAS Onlisans Search with Smart Features
@mcp.tool()
def search_associate_degree_programs(
    # User-friendly parameters with fuzzy matching
    university: str = '',              # University name (supports fuzzy matching like "anadolu", "istanbul")
    program: str = '',                 # Program name (supports partial matching like "bilgisayar", "turizm")
    city: str = '',                    # City name (like "istanbul", "ankara")
    university_type: Literal['', 'Devlet', 'Vakıf', 'KKTC', 'Yurt Dışı'] = '',  # University type
    fee_type: Literal['', 'Ücretsiz', 'Ücretli', 'İÖ-Ücretli', 'Burslu', '%50 İndirimli', '%25 İndirimli', 'AÖ-Ücretli', 'UÖ-Ücretli'] = '',  # Fee/scholarship type
    education_type: Literal['', 'Örgün', 'İkinci', 'Açıköğretim', 'Uzaktan'] = '',  # Education type
    availability: Literal['', 'Doldu', 'Doldu#', 'Dolmadı', 'Yeni'] = '',  # Program availability status
    results_limit: int = 50,           # Number of results to return (default: 50)
    # Legacy parameter support for backward compatibility
    yop_kodu: str = '',
    uni_adi: str = '',
    program_adi: str = '',
    sehir_adi: str = '',
    universite_turu: str = '',
    ucret_burs: str = '',
    ogretim_turu: str = '',
    doluluk: str = '',
    ust_puan: float = 550.0,
    alt_puan: float = 150.0,
    page: int = 1
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
    try:
        if NEW_SMART_API:
            # Use new smart search functions (v0.4.3+)
            search_params = {}
            
            # Map user-friendly parameters to API parameters
            if university or uni_adi:
                search_params['uni_adi'] = university or uni_adi
            if program or program_adi:
                search_params['program_adi'] = program or program_adi
            if city or sehir_adi:
                search_params['city'] = city or sehir_adi
            if university_type or universite_turu:
                search_params['university_type'] = university_type or universite_turu
            if fee_type or ucret_burs:
                search_params['fee_type'] = fee_type or ucret_burs
            if education_type or ogretim_turu:
                search_params['education_type'] = education_type or ogretim_turu
            if results_limit:
                search_params['length'] = results_limit
                
            # Use smart search with fuzzy matching
            results = search_onlisans_programs(search_params, smart_search=True)
            
            # Format results consistently
            return {
                "programs": results,
                "total_found": len(results),
                "search_method": "smart_search_v0.4.3",
                "fuzzy_matching": True,
                "program_type": "associate_degree"
            }
            
        else:
            # Fallback to legacy API
            params = {
                'yop_kodu': yop_kodu,
                'uni_adi': university or uni_adi,
                'program_adi': program or program_adi,
                'sehir_adi': city or sehir_adi,
                'universite_turu': university_type or universite_turu,
                'ucret_burs': fee_type or ucret_burs,
                'ogretim_turu': education_type or ogretim_turu,
                'doluluk': doluluk,
                'ust_puan': ust_puan,
                'alt_puan': alt_puan,
                'page': page
            }
            
            # Remove empty parameters
            params = {k: v for k, v in params.items() if v or isinstance(v, (int, float))}
            
            onlisans_tercih = YOKATLASOnlisansTercihSihirbazi(params)
            result = onlisans_tercih.search()
            
            return {
                "programs": result[:results_limit] if isinstance(result, list) else result,
                "total_found": len(result) if isinstance(result, list) else 0,
                "search_method": "legacy_api",
                "fuzzy_matching": False,
                "program_type": "associate_degree"
            }
            
    except Exception as e:
        print(f"Error in search_associate_degree_programs: {e}")
        return {
            "error": str(e),
            "search_method": "smart_search" if NEW_SMART_API else "legacy_api",
            "parameters_used": {
                "university": university or uni_adi,
                "program": program or program_adi,
                "city": city or sehir_adi
            },
            "program_type": "associate_degree"
        }

def main():
    """Main entry point for the YOKATLAS MCP server."""
    import sys
    
    # Default to stdio transport for MCP compatibility
    transport = "stdio"
    
    # Check if running in development mode
    if "--dev" in sys.argv:
        transport = "sse"
        print("Starting YOKATLAS API MCP Server in development mode...")
        print("Server will be available at http://127.0.0.1:8000")
        mcp.run(transport=transport, host="127.0.0.1", port=8000)
    else:
        # Run with stdio transport for Claude Desktop and other MCP clients
        mcp.run(transport=transport)

if __name__ == "__main__":
    main()