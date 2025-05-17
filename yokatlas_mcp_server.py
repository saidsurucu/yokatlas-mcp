from fastmcp import FastMCP

from yokatlas_py.lisansatlasi import YOKATLASLisansAtlasi
from yokatlas_py.lisanstercihsihirbazi import YOKATLASLisansTercihSihirbazi
from yokatlas_py.onlisansatlasi import YOKATLASOnlisansAtlasi
from yokatlas_py.onlisanstercihsihirbazi import YOKATLASOnlisansTercihSihirbazi


import yokatlas_pdf_generator


mcp = FastMCP(
    name="YOKATLAS_API_Server", description="Provides access to YOKATLAS data via MCP."
)


# Tool for YOKATLAS Onlisans Atlasi
@mcp.tool()
async def get_associate_degree_atlas_details(yop_kodu: str, year: int) -> dict:
    """
    Fetches all details for a specific associate degree program (Önlisans Atlası)
    for a given year. The details include General Information, Quota Placement, Gender Distribution, City Distribution, Geographical Region Distribution, Placement Distribution by City, Placement by City Total, Education Status, Education Status Total, Graduation Year Distribution, Graduation Year Total, High School Field Distribution, High School Field Total, High School Group and Type Distribution, Placement Distribution by High School, High School Valedictorian Placement, Minimum Score and Ranking Statistics, Last Person Placed Information, Average Net Scores of Placed Students, Placement Score Information, Placement Ranking Information, Preference Statistics, Placement Preference Statistics, Preference Usage Rates, Preferred University Types, Preferred Universities, Preferred Cities, Preferred Program Types, Preferred Programs, Academic Staff Numbers, Registered Student Gender Distribution, Graduation Year Gender Distribution, Exchange Program Information, Transfer Information.
    """
    try:
        onlisans_atlasi = YOKATLASOnlisansAtlasi({"program_id": yop_kodu, "year": year})
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
        lisans_atlasi = YOKATLASLisansAtlasi({"program_id": yop_kodu, "year": year})
        result = await lisans_atlasi.fetch_all_details()
        return result
    except Exception as e:
        print(f"Error in get_bachelor_degree_atlas_details: {e}")
        return {"error": str(e), "program_id": yop_kodu, "year": year}


# Tool for YOKATLAS Lisans Tercih Sihirbazi
@mcp.tool()
def search_bachelor_degree_programs(
    yop_kodu: str = "",
    uni_adi: str = "",
    program_adi: str = "",
    sehir_adi: str = "",
    universite_turu: str = "",  # e.g., 'Devlet', 'Vakıf'
    ucret_burs: str = "",  # e.g., 'Ücretsiz', '%100 Burslu', 'Burslu', 'Ücretli'
    ogretim_turu: str = "",  # e.g., 'Örgün', 'İkinci Öğretim'
    doluluk: str = "",  # e.g., '1' (Dolu), '0' (Boş), '' (Tümü)
    puan_turu: str = "SAY",  # e.g., SAY, EA, SOZ, DIL
    ust_bs: int = 0,  # Upper bound for success ranking (Başarı Sırası)
    alt_bs: int = 3000000,  # Lower bound for success ranking
    page: int = 1,
) -> dict:
    """
    Searches for bachelor's degree programs (Lisans Tercih Sihirbazı)
    based on various criteria.
    """
    params = {
        "yop_kodu": yop_kodu,
        "uni_adi": uni_adi,
        "program_adi": program_adi,
        "sehir_adi": sehir_adi,
        "universite_turu": universite_turu,
        "ucret_burs": ucret_burs,
        "ogretim_turu": ogretim_turu,
        "doluluk": doluluk,
        "puan_turu": puan_turu.lower(),  # API might expect lowercase puan_turu
        "ust_bs": ust_bs,
        "alt_bs": alt_bs,
        "page": page,
    }
    try:
        lisans_tercih = YOKATLASLisansTercihSihirbazi(params)
        result = lisans_tercih.search()
        return result
    except Exception as e:
        print(f"Error in search_bachelor_degree_programs: {e}")
        return {"error": str(e), "params_used": params}


# Tool for YOKATLAS Onlisans Tercih Sihirbazi
@mcp.tool()
def search_associate_degree_programs(
    yop_kodu: str = "",
    uni_adi: str = "",
    program_adi: str = "",
    sehir_adi: str = "",
    universite_turu: str = "",  # e.g., 'Devlet', 'Vakıf'
    ucret_burs: str = "",  # e.g., 'Ücretsiz', '%100 Burslu', 'Burslu', 'Ücretli'
    ogretim_turu: str = "",  # e.g., 'Örgün', 'İkinci Öğretim'
    doluluk: str = "",  # e.g., '1' (Dolu), '0' (Boş), '' (Tümü)
    ust_puan: float = 550.0,  # Upper bound for score (Puan)
    alt_puan: float = 150.0,  # Lower bound for score
    page: int = 1,
) -> dict:
    """
    Searches for associate degree programs (Önlisans Tercih Sihirbazı)
    based on various criteria.
    """
    params = {
        "yop_kodu": yop_kodu,
        "uni_adi": uni_adi,
        "program_adi": program_adi,
        "sehir_adi": sehir_adi,
        "universite_turu": universite_turu,
        "ucret_burs": ucret_burs,
        "ogretim_turu": ogretim_turu,
        "doluluk": doluluk,
        "ust_puan": ust_puan,
        "alt_puan": alt_puan,
        "page": page,
    }
    try:
        onlisans_tercih = YOKATLASOnlisansTercihSihirbazi(params)
        result = onlisans_tercih.search()
        return result
    except Exception as e:
        print(f"Error in search_associate_degree_programs: {e}")
        return {"error": str(e), "params_used": params}


# Tool for generating PDF Reports from search results
@mcp.tool()
def generate_pdf_report(
    data: dict,
    report_type: str,
    title: str = "YOKATLAS Raporu",
    language: str = "tr",  # 'tr' for Turkish, 'en' for English (future support)
    save_to_downloads: bool = True,
) -> dict:
    """
    Generates a formatted PDF report from YOKATLAS data.

    Parameters:
    - data: The data dictionary from one of the YOKATLAS search or details functions
    - report_type: Type of report ('bachelor_search', 'associate_search', 'bachelor_details', 'associate_details')
    - title: Custom title for the report
    - language: Report language ('tr' for Turkish, 'en' for English - future)
    - save_to_downloads: If True, saves the PDF to the user's Downloads folder

    Returns:
    - A dictionary containing the Base64 encoded PDF content, filename, and local path where saved
    """
    try:
        output_dir = None
        if save_to_downloads:
            output_dir = yokatlas_pdf_generator.get_downloads_folder()

        result = yokatlas_pdf_generator.generate_pdf(
            data=data,
            report_type=report_type,
            title=title,
            language=language,
            save_to_local=True,
            output_dir=output_dir,
        )

        if result["success"] and result["local_path"]:
            result["claude_message"] = f"Downloaded PDF file: {result['local_path']}"

        return result

    except Exception as e:
        error_msg = str(e)
        print(f"Error in generate_pdf_report: {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "message": "PDF rapor oluşturma sırasında hata oluştu.",
        }


if __name__ == "__main__":
    print("Starting YOKATLAS API MCP Server...")
    print("To run this server with FastMCP CLI: fastmcp run yokatlas_mcp_server.py")
    print(
        "Or to run directly (e.g., with SSE on port 8000): python yokatlas_mcp_server.py"
    )

    # To run with default stdio transport:
    # mcp.run()

    # Example: Run with SSE transport on a specific port
    # This makes it accessible over HTTP for MCP clients that support SSE.
    mcp.run(transport="sse", host="127.0.0.1", port=8000)
