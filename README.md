# YOKATLAS API MCP Sunucusu

[![Star History Chart](https://api.star-history.com/svg?repos=saidsurucu/yokatlas-mcp&type=Date)](https://www.star-history.com/#saidsurucu/yokatlas-mcp&Date)

Bu proje, [YÖKATLAS](https://yokatlas.yok.gov.tr/) verilerine erişimi sağlayan `yokatlas-py` Python kütüphanesini kullanarak bir [FastMCP](https://www.gofastmcp.com/) sunucusu oluşturur. Bu sayede, YÖKATLAS API fonksiyonları, Model Context Protocol (MCP) destekleyen LLM (Büyük Dil Modeli) uygulamaları ve diğer istemciler tarafından araç (tool) olarak kullanılabilir hale gelir.

![örnek](./ornek.png)

## 🎯 Temel Özellikler

* YÖKATLAS verilerine programatik erişim için standart bir MCP arayüzü.
* Lisans ve Önlisans program detaylarını getirme.
* Lisans ve Önlisans programları için kapsamlı arama yapabilme (Tercih Sihirbazı).
* Claude Desktop uygulaması ile kolay entegrasyon.

## 📋 Ön Gereksinimler

* **Python Sürümü:** Python 3.12 veya daha yeni bir sürümünün sisteminizde kurulu olması gerekmektedir. Python'ı [python.org](https://www.python.org/downloads/) adresinden indirebilirsiniz.
* **pip:** Python ile birlikte gelen `pip` paket yöneticisinin çalışır durumda olması gerekir.

<details>
<summary>⚙️ Kurulum Adımları</summary>

### Hızlı Kurulum (Önerilen)

Claude Desktop'a entegre etmek için sadece `uv` kurulumuna ihtiyacınız var:

#### 1. `uv` Kurulumu
`uv`, hızlı bir Python paket yöneticisidir.

* **macOS ve Linux:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

* **Windows (PowerShell):**
  ```bash
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

* **pip ile kurulum:**
  ```bash
  pip install uv
  ```

Kurulumu doğrulayın: `uv --version`

#### 2. Claude Desktop'a Ekleme

Claude Desktop ayarlarından (Settings > Developer > Edit Config) yapılandırma dosyasına aşağıdaki girdiyi ekleyin:

```json
{
  "mcpServers": {
    "YOKATLAS API Servisi": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/saidsurucu/yokatlas-mcp",
        "yokatlas-mcp"
      ]
    }
  }
}
```

Başarılı bir kurulumdan sonra, Claude Desktop uygulamasında YOKATLAS API araçlarını kullanabilirsiniz.

</details>

<details>
<summary>🚀 Claude Haricindeki Modellerle Kullanmak İçin Çok Kolay Kurulum (Örnek: 5ire için)</summary>

Bu bölüm, YOKATLAS MCP aracını 5ire gibi Claude Desktop dışındaki MCP istemcileriyle kullanmak isteyenler içindir.

1. **Python Kurulumu:** Sisteminizde Python 3.12 veya üzeri kurulu olmalıdır. Kurulum sırasında "Add Python to PATH" (Python'ı PATH'e ekle) seçeneğini işaretlemeyi unutmayın. [Buradan indirebilirsiniz](https://www.python.org/downloads/).

2. **Git Kurulumu (Windows):** Bilgisayarınıza git yazılımını [indirip kurun](https://git-scm.com/download/win). "Git for Windows/x64 Setup" seçeneğini indirmelisiniz.

3. **uv Kurulumu:**
   - **Windows Kullanıcıları (PowerShell):** Bir CMD ekranı açın ve bu kodu çalıştırın: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - **Mac/Linux Kullanıcıları (Terminal):** Bir Terminal ekranı açın ve bu kodu çalıştırın: `curl -LsSf https://astral.sh/uv/install.sh | sh`

4. **Microsoft Visual C++ Redistributable (Windows):** Bazı Python paketlerinin doğru çalışması için gereklidir. [Buradan indirip kurun](https://aka.ms/vs/17/release/vc_redist.x64.exe).

5. İşletim sisteminize uygun 5ire MCP istemcisini indirip kurun.

6. 5ire'ı açın. **Workspace → Providers** menüsünden kullanmak istediğiniz LLM servisinin API anahtarını girin.

7. **Tools** menüsüne girin. **+Local** veya **New** yazan butona basın.

8. Aşağıdaki bilgileri girin:
   - **Tool Key:** `yokatlasmcp`
   - **Name:** `YOKATLAS MCP`
   - **Command:**
     ```
     uvx --from git+https://github.com/saidsurucu/yokatlas-mcp yokatlas-mcp
     ```

9. **Save** butonuna basarak kaydedin.

10. Şimdi **Tools** altında **YOKATLAS MCP**'yi görüyor olmalısınız. Üstüne geldiğinizde sağda çıkan butona tıklayıp etkinleştirin (yeşil ışık yanmalı).

11. Artık YOKATLAS MCP ile konuşabilirsiniz.

</details>

<details>
<summary>🔧 Gemini CLI ile Kullanmak İçin Kurulum</summary>

**Video Rehber:** [Gemini CLI MCP Kurulum Videosu](https://youtu.be/mP_4ulb81zw)

**Ön Gereksinimler:** Python, uv, (Windows için) Microsoft Visual C++ Redistributable'ın sisteminizde kurulu olduğundan emin olun. Detaylı bilgi için yukarıdaki "5ire için Kurulum" bölümündeki ilgili adımlara bakabilirsiniz.

1. **Gemini CLI ayarlarını yapılandırın:**

   Gemini CLI'ın ayar dosyasını düzenleyin:
   - **macOS/Linux:** `~/.gemini/settings.json`
   - **Windows:** `%USERPROFILE%\.gemini\settings.json`

2. **Aşağıdaki mcpServers bloğunu ekleyin:**

   ```json
   {
     "theme": "Default",
     "selectedAuthType": "oauth-personal",
     "mcpServers": {
       "yokatlas_mcp": {
         "command": "uvx",
         "args": [
           "--from",
           "git+https://github.com/saidsurucu/yokatlas-mcp",
           "yokatlas-mcp"
         ]
       }
     }
   }
   ```

3. **Yapılandırma açıklamaları:**
   - `"yokatlas_mcp"`: Sunucunuz için yerel bir isim
   - `"command"`: uvx komutu (uv'nin paket çalıştırma aracı)
   - `"args"`: GitHub'dan doğrudan YOKATLAS MCP'yi çalıştırmak için gerekli argümanlar

4. **Kullanım:**
   - Gemini CLI'ı başlatın
   - YOKATLAS MCP araçları otomatik olarak kullanılabilir olacaktır
   - **Örnek komutlar:**
     - "İstanbul'daki tıp fakültelerinin 2024 taban puanlarını getir"
     - "Boğaziçi Üniversitesi Bilgisayar Mühendisliği programının detaylarını ara"
     - "SAY puan türünde 400-500 bin sıralama aralığındaki mühendislik programlarını listele"

</details>

## 🛠️ Kullanılabilir Araçlar (MCP Tools)

Bu FastMCP sunucusu aşağıdaki araçları sunar:

1.  **`get_associate_degree_atlas_details`**
    * **Açıklama:** Belirli bir önlisans programının (Önlisans Atlası) verilen yıldaki tüm detaylarını getirir.
    * **Parametreler:** `program_id: str`, `year: int`

2.  **`get_bachelor_degree_atlas_details`**
    * **Açıklama:** Belirli bir lisans programının (Lisans Atlası) verilen yıldaki tüm detaylarını getirir.
    * **Parametreler:** `program_id: str`, `year: int`

3.  **`search_bachelor_degree_programs`**
    * **Açıklama:** Çeşitli kriterlere göre lisans programlarını (Lisans Tercih Sihirbazı) arar.
    * **Parametreler:** `uni_adi: str`, `program_adi: str`, `puan_turu: str` (örn: SAY, EA), `alt_bs: int`, `ust_bs: int` vb. (Detaylar için `yokatlas_mcp_server.py` script'indeki tool tanımına bakınız.)

4.  **`search_associate_degree_programs`**
    * **Açıklama:** Çeşitli kriterlere göre önlisans programlarını (Önlisans Tercih Sihirbazı) arar.
    * **Parametreler:** `uni_adi: str`, `program_adi: str`, `alt_puan: float`, `ust_puan: float` vb. (Detaylar için `yokatlas_mcp_server.py` script'indeki tool tanımına bakınız.)


## 📜 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.