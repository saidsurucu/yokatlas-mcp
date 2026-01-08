# YOKATLAS MCP: Türk Yükseköğretim Atlası için MCP Sunucusu

Bu proje, [YÖKATLAS](https://yokatlas.yok.gov.tr/) verilerine erişimi kolaylaştıran bir [FastMCP](https://gofastmcp.com/) sunucusu oluşturur. Bu sayede, YÖKATLAS'tan lisans ve önlisans program arama ve detaylı istatistik getirme işlemleri, Model Context Protocol (MCP) destekleyen LLM (Büyük Dil Modeli) uygulamaları (örneğin Claude Desktop veya [5ire](https://5ire.app)) ve diğer istemciler tarafından araç (tool) olarak kullanılabilir hale gelir.

![YOKATLAS MCP Örneği](./ornek.png)

🎯 **Temel Özellikler**

* YÖKATLAS verilerine programatik erişim için standart bir MCP arayüzü.
* Aşağıdaki yetenekler:
    * **Akıllı Program Arama:** Fuzzy matching ile üniversite ve program adı arama (örn: "boğaziçi" → "BOĞAZİÇİ ÜNİVERSİTESİ")
    * **Lisans Program Detayları:** Kontenjan, yerleşme puanları, öğrenci demografisi, akademik kadro bilgileri
    * **Önlisans Program Detayları:** Kontenjan, yerleşme verileri, tesis bilgileri
    * **Kapsamlı Filtreleme:** Şehir, üniversite türü, ücret durumu, öğretim türü
* Claude Desktop uygulaması ile `fastmcp install` komutu (veya manuel yapılandırma) kullanılarak kolay entegrasyon.
* YOKATLAS MCP [5ire](https://5ire.app) gibi Claude Desktop haricindeki MCP istemcilerini de destekler.

---

## 🚀 5 Dakikada Başla (Remote MCP)

### ✅ Kurulum Gerektirmez! Hemen Kullan!

🔗 **Remote MCP Adresi:** `https://yokatlasmcp.fastmcp.app/mcp`

### Claude Desktop ile Kullanım

1. **Claude Desktop'ı açın**
2. **Settings → Connectors → Add Custom Connector**
3. **Bilgileri girin:**
   - **Name:** `YOKATLAS MCP`
   - **URL:** `https://yokatlasmcp.fastmcp.app/mcp`
4. **Add** butonuna tıklayın
5. **Hemen kullanmaya başlayın!** 🎉

### Google Antigravity ile Kullanım

1. **Agent session** açın ve editörün yan panelindeki **"…"** dropdown menüsüne tıklayın
2. **MCP Servers** seçeneğini seçin - MCP Store açılacak
3. Üstteki **Manage MCP Servers** butonuna tıklayın
4. **View raw config** seçeneğine tıklayın
5. `mcp_config.json` dosyasına aşağıdaki yapılandırmayı ekleyin:

```json
{
  "mcpServers": {
    "yokatlas-mcp": {
      "serverUrl": "https://yokatlasmcp.fastmcp.app/mcp/",
      "headers": {
        "Content-Type": "application/json"
      }
    }
  }
}
```

> 💡 **İpucu:** Remote MCP sayesinde Python, uv veya herhangi bir kurulum yapmadan doğrudan Claude Desktop üzerinden YÖKATLAS verilerine erişebilirsiniz!

---

## 🚀 Claude Haricindeki Modellerle Kullanmak İçin Çok Kolay Kurulum (Örnek: 5ire için)

Bu bölüm, YOKATLAS MCP aracını 5ire gibi Claude Desktop dışındaki MCP istemcileriyle kullanmak isteyenler içindir.

* **Python Kurulumu:** Sisteminizde Python 3.12 kurulu olmalıdır. Kurulum sırasında "**Add Python to PATH**" (Python'ı PATH'e ekle) seçeneğini işaretlemeyi unutmayın. [Buradan](https://www.python.org/downloads/) indirebilirsiniz.
* **Git Kurulumu (Windows):** Bilgisayarınıza [git](https://git-scm.com/downloads/win) yazılımını indirip kurun. "Git for Windows/x64 Setup" seçeneğini indirmelisiniz.
* **`uv` Kurulumu:**
    * **Windows Kullanıcıları (PowerShell):** Bir CMD ekranı açın ve bu kodu çalıştırın: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
    * **Mac/Linux Kullanıcıları (Terminal):** Bir Terminal ekranı açın ve bu kodu çalıştırın: `curl -LsSf https://astral.sh/uv/install.sh | sh`
* **Microsoft Visual C++ Redistributable (Windows):** Bazı Python paketlerinin doğru çalışması için gereklidir. [Buradan](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170) indirip kurun.
* İşletim sisteminize uygun [5ire](https://5ire.app) MCP istemcisini indirip kurun.
* 5ire'ı açın. **Workspace -> Providers** menüsünden kullanmak istediğiniz LLM servisinin API anahtarını girin.
* **Tools** menüsüne girin. **+Local** veya **New** yazan butona basın.
    * **Tool Key:** `yokatlasmcp`
    * **Name:** `YOKATLAS MCP`
    * **Command:**
        ```
        uvx --from git+https://github.com/saidsurucu/yokatlas-mcp yokatlas-mcp
        ```
    * **Save** butonuna basarak kaydedin.

* Şimdi **Tools** altında **YOKATLAS MCP**'yi görüyor olmalısınız. Üstüne geldiğinizde sağda çıkan butona tıklayıp etkinleştirin (yeşil ışık yanmalı).
* Artık YOKATLAS MCP ile konuşabilirsiniz.

---

## ⚙️ Claude Desktop Manuel Kurulumu

1.  **Ön Gereksinimler:** Python, `uv`, (Windows için) Microsoft Visual C++ Redistributable'ın sisteminizde kurulu olduğundan emin olun. Detaylı bilgi için yukarıdaki "5ire için Kurulum" bölümündeki ilgili adımlara bakabilirsiniz.
2.  Claude Desktop **Settings -> Developer -> Edit Config**.
3.  Açılan `claude_desktop_config.json` dosyasına `mcpServers` altına ekleyin:

    ```json
    {
      "mcpServers": {
        "YOKATLAS MCP": {
          "command": "uvx",
          "args": [
            "--from", "git+https://github.com/saidsurucu/yokatlas-mcp",
            "yokatlas-mcp"
          ]
        }
      }
    }
    ```

4.  Claude Desktop'ı kapatıp yeniden başlatın.

---

## 🛠️ Kullanılabilir Araçlar (MCP Tools)

Bu FastMCP sunucusu LLM modelleri için aşağıdaki araçları sunar:

### 🔍 Akıllı Arama Araçları

* **`search_bachelor_degree_programs`**: Lisans programları için akıllı arama (Fuzzy matching ile)
    * **Özellikler:** Fuzzy matching ("boğaziçi" → "BOĞAZİÇİ ÜNİVERSİTESİ"), kısmi eşleştirme ("bilgisayar" → tüm bilgisayar programları)
    * **Parametreler**: `university`, `program`, `city`, `score_type` (SAY/EA/SOZ/DIL), `university_type`, `fee_type`, `education_type`, `availability`, `results_limit`

* **`search_associate_degree_programs`**: Önlisans programları için akıllı arama (Fuzzy matching ile)
    * **Özellikler:** Fuzzy matching, kısmi eşleştirme, TYT puan sistemi desteği
    * **Parametreler**: `university`, `program`, `city`, `university_type`, `fee_type`, `education_type`, `availability`, `results_limit`

### 📊 Atlas Detay Araçları

* **`get_bachelor_degree_atlas_details`**: Belirli bir lisans programının kapsamlı detaylarını getirir
    * **Parametreler**: `yop_kodu` (Program YÖP kodu), `year` (Veri yılı: 2025, 2024, 2023)
    * **Döndürülen Veriler**: Kontenjan, yerleşme puanları, öğrenci demografisi, akademik kadro, tesis bilgileri

* **`get_associate_degree_atlas_details`**: Belirli bir önlisans programının kapsamlı detaylarını getirir
    * **Parametreler**: `yop_kodu` (Program YÖP kodu), `year` (Veri yılı: 2025, 2024, 2023)
    * **Döndürülen Veriler**: Kontenjan, yerleşme verileri, öğrenci dağılımı, akademik kadro bilgileri

---

## 📜 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.
