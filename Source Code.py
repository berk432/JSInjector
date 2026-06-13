import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import messagebox
import time
import traceback
from datetime import datetime

class JsInjectorApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("JavaScript Injector - berk432")
        self.window.geometry("900x800")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Site URL
        self.url_label = ctk.CTkLabel(self.window, text="Hedef Site URL:", font=("Arial", 14))
        self.url_label.pack(pady=(10, 0))
        
        self.url_entry = ctk.CTkEntry(self.window, width=600, placeholder_text="https://example.com")
        self.url_entry.pack(pady=5)
        
        # JavaScript kodu
        self.js_label = ctk.CTkLabel(self.window, text="JavaScript Kodu (Inject edilecek):", font=("Arial", 14))
        self.js_label.pack(pady=(10, 0))
        
        self.js_text = ctk.CTkTextbox(self.window, width=800, height=200)
        self.js_text.pack(pady=5)
        
        # Örnek kod
        self.js_text.insert("1.0", """// Sayfaya bir div ekle
try {
    var div = document.createElement('div');
    div.innerHTML = '<h2 style="color:lime">🔥 INJECT EDİLDİ! 🔥</h2>';
    div.style.position = 'fixed';
    div.style.top = '20px';
    div.style.right = '20px';
    div.style.background = 'black';
    div.style.padding = '20px';
    div.style.borderRadius = '10px';
    div.style.zIndex = '99999';
    document.body.appendChild(div);
    console.log('Inject başarılı!');
} catch(e) {
    console.error('Inject hatası:', e);
}""")
        
        # Butonlar
        self.button_frame = ctk.CTkFrame(self.window)
        self.button_frame.pack(pady=15)
        
        self.inject_btn = ctk.CTkButton(self.button_frame, text="🚀 OTOMATIK INJECT ET", 
                                         command=self.auto_inject, height=45, font=("Arial", 15))
        self.inject_btn.pack(side="left", padx=10)
        
        self.close_btn = ctk.CTkButton(self.button_frame, text="❌ TARAYICIYI KAPAT", 
                                        command=self.close_browser, height=45, fg_color="darkred")
        self.close_btn.pack(side="left", padx=10)
        
        self.clear_btn = ctk.CTkButton(self.button_frame, text="🗑 DEBUG TEMİZLE", 
                                        command=self.clear_debug, height=45, fg_color="darkorange")
        self.clear_btn.pack(side="left", padx=10)
        
        # Durum etiketi
        self.status_label = ctk.CTkLabel(self.window, text="✅ Hazır", font=("Arial", 12), text_color="green")
        self.status_label.pack(pady=5)
        
        # DEBUG ALANI
        self.debug_label = ctk.CTkLabel(self.window, text="🔍 DEBUG / HATA ALANI:", font=("Arial", 14, "bold"))
        self.debug_label.pack(pady=(15, 0))
        
        self.debug_text = ctk.CTkTextbox(self.window, width=850, height=250, font=("Consolas", 11))
        self.debug_text.pack(pady=5)
        
        # Driver referansı
        self.driver = None
        
        # İlk debug mesajı
        self.add_debug("INFO", "Uygulama başlatıldı, hazır beklemede. - by berk432")
        
        self.window.mainloop()
    
    def add_debug(self, level, message, error_detail=None):
        """Debug alanına mesaj ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if level == "ERROR":
            emoji = "❌"
        elif level == "WARNING":
            emoji = "⚠️"
        elif level == "SUCCESS":
            emoji = "✅"
        else:
            emoji = "ℹ️"
        
        debug_line = f"[{timestamp}] {emoji} [{level}] {message}\n"
        
        if error_detail:
            debug_line += f"     📎 Detay: {error_detail}\n"
        
        self.debug_text.insert("end", debug_line)
        self.debug_text.see("end")
        self.window.update()
    
    def clear_debug(self):
        """Debug alanını temizle"""
        self.debug_text.delete("1.0", "end")
        self.add_debug("INFO", "Debug alanı temizlendi.")
    
    def close_browser(self):
        """Tarayıcıyı manuel kapat"""
        if self.driver:
            self.add_debug("INFO", "Tarayıcı kapatılıyor...")
            self.driver.quit()
            self.driver = None
            self.add_debug("SUCCESS", "Tarayıcı kapatıldı.")
            self.status_label.configure(text="✅ Tarayıcı kapalı", text_color="green")
        else:
            self.add_debug("WARNING", "Zaten açık bir tarayıcı yok.")
    
    def auto_inject(self):
        url = self.url_entry.get().strip()
        if not url:
            self.add_debug("ERROR", "URL girilmedi!")
            messagebox.showerror("Hata", "URL gir lütfen!")
            return
        
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            self.add_debug("INFO", f"URL düzeltildi: {url}")
        
        js_code = self.js_text.get("1.0", "end-1c").strip()
        if not js_code:
            self.add_debug("ERROR", "JavaScript kodu boş!")
            messagebox.showerror("Hata", "JavaScript kodu gir!")
            return
        
        self.add_debug("INFO", f"Inject işlemi başlatılıyor: {url}")
        self.status_label.configure(text="🚀 İşlem başladı...", text_color="yellow")
        self.window.update()
        
        try:
            # Eğer driver varsa ve açıksa kullan, yoksa yeni aç
            if self.driver is None:
                self.add_debug("INFO", "Yeni Chrome driver başlatılıyor...")
                chrome_options = Options()
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                self.add_debug("SUCCESS", "Chrome driver başarıyla başlatıldı.")
            else:
                self.add_debug("INFO", "Mevcut tarayıcı kullanılıyor.")
            
            # Siteyi aç
            self.add_debug("INFO", f"Site açılıyor: {url}")
            self.driver.get(url)
            self.add_debug("SUCCESS", f"Site açıldı: {url}")
            
            time.sleep(2)
            
            # JavaScript inject et
            self.add_debug("INFO", "JavaScript kodu inject ediliyor...")
            try:
                result = self.driver.execute_script(js_code)
                if result:
                    self.add_debug("SUCCESS", f"JS inject edildi. Return değeri: {result}")
                else:
                    self.add_debug("SUCCESS", "JS inject edildi.")
            except Exception as js_error:
                error_msg = str(js_error)
                self.add_debug("ERROR", "JavaScript çalıştırılamadı!", error_msg)
                raise js_error
            
            self.status_label.configure(text="✅ INJECT BAŞARILI! Tarayıcı açık kalacak.", text_color="lime")
            self.add_debug("SUCCESS", "========== İŞLEM TAMAMLANDI ==========")
            self.add_debug("INFO", "Tarayıcı AÇIK KALACAK. Kapatmak için 'TARAYICIYI KAPAT' butonuna bas.")
            
            # Konsol loglarını al
            try:
                logs = self.driver.get_log('browser')
                if logs:
                    self.add_debug("INFO", f"Tarayıcı konsolunda {len(logs)} adet log var:")
                    for log in logs[-5:]:
                        self.add_debug("INFO", f"  Konsol: {log.get('message', '')[:200]}")
            except:
                pass
            
            messagebox.showinfo("Başarılı!", "JavaScript kodu siteye inject edildi!\nTarayıcı AÇIK KALACAK.\nKapatmak için 'TARAYICIYI KAPAT' butonuna bas.")
            
        except Exception as e:
            error_trace = traceback.format_exc()
            self.add_debug("ERROR", f"BEKLEMEDİK HATA!", str(e))
            self.add_debug("ERROR", f"Traceback:\n{error_trace[:500]}")
            self.status_label.configure(text="❌ HATA OLUŞTU! Debug alanına bak.", text_color="red")
            messagebox.showerror("Hata", f"Bir şeyler yanlış gitti!\n\n{str(e)}\n\nDetaylar debug alanında.")

if __name__ == "__main__":
    app = JsInjectorApp()
