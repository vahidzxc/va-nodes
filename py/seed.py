import random
from typing import Any, Dict, Optional

SEED_MAX_VALUE = 2**40

class VA_Seed:
    def __init__(self) -> None:
        self._random = random.Random()
        self._last_seed = None
        self.force_run = False
        
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "seed": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": SEED_MAX_VALUE
                }),
                "previous_seed": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": SEED_MAX_VALUE,
                    "readonly": True
                }),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "my_unique_id": "UNIQUE_ID"
            }
        }
        
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("seed",)
    FUNCTION = "process"
    CATEGORY = "Seed"
    
    def process(self, 
                seed: int = 0,
                previous_seed: int = 0,
                prompt: Optional[str] = None,
                extra_pnginfo: Optional[Dict] = None,
                my_unique_id: Optional[str] = None) -> tuple:
        
        # اگر seed تغییر کرده، force_run را فعال می‌کنیم
        if self._last_seed != seed:
            self.force_run = True
        
        # ذخیره seed فعلی برای مقایسه بعدی
        self._last_seed = seed
        return (seed,)
        
    @classmethod
    def IS_CHANGED(cls, **kwargs) -> float:
        """کنترل اجرای مجدد نود"""
        # وقتی force_run فعال است، اجازه اجرای مجدد می‌دهیم
        if hasattr(cls, 'force_run') and cls.force_run:
            cls.force_run = False  # ریست کردن وضعیت
            return float("nan")
        return 0  # در غیر این صورت از اجرای مجدد جلوگیری می‌کنیم

# Node registration
NODE_CLASS_MAPPINGS = {
    "VA_Seed": VA_Seed
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VA_Seed": "VA Seed"
}