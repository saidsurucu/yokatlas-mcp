import asyncio  # Required for async yokatlas_py functions

from fastmcp import FastMCP

# Import the YOKATLAS-py classes with new API structure
try:
    from yokatlas_py import YOKATLASLisansTercihSihirbazi, YOKATLASOnlisansTercihSihirbazi
    from yokatlas_py import YOKATLASLisansAtlasi, YOKATLASOnlisansAtlasi
    NEW_API = True
except ImportError:
    # Fallback to old import structure
    from yokatlas_py.lisansatlasi import YOKATLASLisansAtlasi
    from yokatlas_py.lisanstercihsihirbazi import YOKATLASLisansTercihSihirbazi
    from yokatlas_py.onlisansatlasi import YOKATLASOnlisansAtlasi
    from yokatlas_py.onlisanstercihsihirbazi import YOKATLASOnlisansTercihSihirbazi
    NEW_API = False

# Try to import models for new API
try:
    from yokatlas_py.models import SearchParams, ProgramInfo
    HAS_MODELS = True
except ImportError:
    HAS_MODELS = False

# Create a FastMCP server instance
mcp = FastMCP("YOKATLAS API Server")

# Tool for YOKATLAS Onlisans Atlasi
@mcp.tool()
async def get_associate_degree_atlas_details(yop_kodu: str, year: int) -> dict:
    """
    Fetches all details for a specific associate degree program (Önlisans Atlası)
    for a given year. The details include General Information, Quota Placement, Gender Distribution, City Distribution, Geographical Region Distribution, Placement Distribution by City, Placement by City Total, Education Status, Education Status Total, Graduation Year Distribution, Graduation Year Total, High School Field Distribution, High School Field Total, High School Group and Type Distribution, Placement Distribution by High School, High School Valedictorian Placement, Minimum Score and Ranking Statistics, Last Person Placed Information, Average Net Scores of Placed Students, Placement Score Information, Placement Ranking Information, Preference Statistics, Placement Preference Statistics, Preference Usage Rates, Preferred University Types, Preferred Universities, Preferred Cities, Preferred Program Types, Preferred Programs, Academic Staff Numbers, Registered Student Gender Distribution, Graduation Year Gender Distribution, Exchange Program Information, Transfer Information.
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
    Fetches all details for a specific bachelor's degree program (Lisans Atlası)
    for a given year. The details include General Information, Quota Placement, Gender Distribution, City Distribution, Geographical Region Distribution, Placement Distribution by City, Placement by City Total, Education Status, Education Status Total, Graduation Year Distribution, Graduation Year Total, High School Field Distribution, High School Field Total, High School Group and Type Distribution, Placement Distribution by High School, High School Valedictorian Placement, Minimum Score and Ranking Statistics, Last Person Placed Information, Average Net Scores of Placed Students, Placement Score Information, Placement Ranking Information, Preference Statistics, Placement Preference Statistics, Preference Usage Rates, Preferred University Types, Preferred Universities, Preferred Cities, Preferred Program Types, Preferred Programs, Academic Staff Numbers, Registered Student Gender Distribution, Graduation Year Gender Distribution, Exchange Program Information, Transfer Information.
    """
    try:
        lisans_atlasi = YOKATLASLisansAtlasi({'program_id': yop_kodu, 'year': year})
        result = await lisans_atlasi.fetch_all_details()
        return result
    except Exception as e:
        print(f"Error in get_bachelor_degree_atlas_details: {e}")
        return {"error": str(e), "program_id": yop_kodu, "year": year}

# Tool for YOKATLAS Lisans Tercih Sihirbazi
@mcp.tool()
def search_bachelor_degree_programs(
    # New API parameters (used if available)
    sehir: str = '',          # City name for new API
    length: int = 10,         # Number of results for new API
    puan_turu: str = 'SAY',   # Score type for new API
    # Legacy parameters (backward compatibility)
    yop_kodu: str = '',
    uni_adi: str = '',
    program_adi: str = '',
    sehir_adi: str = '',
    universite_turu: str = '', # e.g., 'Devlet', 'Vakıf'
    ucret_burs: str = '',     # e.g., 'Ücretsiz', '%100 Burslu', 'Burslu', 'Ücretli'
    ogretim_turu: str = '',   # e.g., 'Örgün', 'İkinci Öğretim'
    doluluk: str = '',        # e.g., '1' (Dolu), '0' (Boş), '' (Tümü)
    ust_bs: int = 0,          # Upper bound for success ranking (Başarı Sırası)
    alt_bs: int = 3000000,    # Lower bound for success ranking
    page: int = 1
) -> dict:
    """
    Searches for bachelor's degree programs (Lisans Tercih Sihirbazı)
    based on various criteria. Supports both new and legacy API parameters.
    
    New API parameters: sehir, length, puan_turu
    Legacy parameters: yop_kodu, uni_adi, program_adi, sehir_adi, etc.
    """
    try:
        if HAS_MODELS and NEW_API:
            # Use new API with models if available
            new_params = {}
            if sehir:
                new_params['sehir'] = sehir
            if length and length != 10:
                new_params['length'] = length
            if puan_turu:
                new_params['puan_turu'] = puan_turu.lower()
            if universite_turu:
                new_params['universite_turu'] = universite_turu
                
            # Try SearchParams validation
            try:
                validated_params = SearchParams(**new_params)
                search_params = validated_params.model_dump(exclude_none=True)
            except:
                # Fallback to direct params if validation fails
                search_params = new_params
                
            lisans_tercih = YOKATLASLisansTercihSihirbazi(search_params)
            result = lisans_tercih.search()
            
            # Try to validate results with ProgramInfo if available
            try:
                validated_results = []
                for item in result[:length] if isinstance(result, list) else []:
                    try:
                        program = ProgramInfo(**item)
                        validated_results.append(program.model_dump())
                    except:
                        validated_results.append(item)
                return {"data": validated_results, "total": len(validated_results)}
            except:
                return result
        else:
            # Use legacy API parameters
            params = {
                'yop_kodu': yop_kodu,
                'uni_adi': uni_adi,
                'program_adi': program_adi,
                'sehir_adi': sehir_adi or sehir,  # Use sehir if sehir_adi is empty
                'universite_turu': universite_turu,
                'ucret_burs': ucret_burs,
                'ogretim_turu': ogretim_turu,
                'doluluk': doluluk,
                'puan_turu': puan_turu.lower(),
                'ust_bs': ust_bs,
                'alt_bs': alt_bs,
                'page': page
            }
            
            lisans_tercih = YOKATLASLisansTercihSihirbazi(params)
            result = lisans_tercih.search()
            return result
            
    except Exception as e:
        print(f"Error in search_bachelor_degree_programs: {e}")
        return {"error": str(e), "new_api": NEW_API, "has_models": HAS_MODELS}

# Tool for YOKATLAS Onlisans Tercih Sihirbazi
@mcp.tool()
def search_associate_degree_programs(
    yop_kodu: str = '',
    uni_adi: str = '',
    program_adi: str = '',
    sehir_adi: str = '',
    universite_turu: str = '', # e.g., 'Devlet', 'Vakıf'
    ucret_burs: str = '',     # e.g., 'Ücretsiz', '%100 Burslu', 'Burslu', 'Ücretli'
    ogretim_turu: str = '',   # e.g., 'Örgün', 'İkinci Öğretim'
    doluluk: str = '',        # e.g., '1' (Dolu), '0' (Boş), '' (Tümü)
    ust_puan: float = 550.0,    # Upper bound for score (Puan)
    alt_puan: float = 150.0,    # Lower bound for score
    page: int = 1
) -> dict:
    """
    Searches for associate degree programs (Önlisans Tercih Sihirbazı)
    based on various criteria.
    """
    params = {
        'yop_kodu': yop_kodu,
        'uni_adi': uni_adi,
        'program_adi': program_adi,
        'sehir_adi': sehir_adi,
        'universite_turu': universite_turu,
        'ucret_burs': ucret_burs,
        'ogretim_turu': ogretim_turu,
        'doluluk': doluluk,
        'ust_puan': ust_puan,
        'alt_puan': alt_puan,
        'page': page
    }
    try:
        onlisans_tercih = YOKATLASOnlisansTercihSihirbazi(params)
        result = onlisans_tercih.search()
        return result
    except Exception as e:
        print(f"Error in search_associate_degree_programs: {e}")
        return {"error": str(e), "params_used": params}

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