import json
import random

random.seed(42)

MONTHS = ["March 2026", "April 2026", "May 2026", "June 2026", "July 2026", "August 2026"]

CATALOG = {
    "Smartphones": {
        "brands": {
            "Apple": ["iPhone 15", "iPhone 15 Pro", "iPhone 15 Pro Max", "iPhone 14", "iPhone SE (2024)"],
            "Samsung": ["Galaxy S24", "Galaxy S24 Ultra", "Galaxy S24+", "Galaxy A55", "Galaxy Z Fold 5", "Galaxy Z Flip 5", "Galaxy M35"],
            "OnePlus": ["OnePlus 12", "OnePlus 12R", "OnePlus Nord 4", "OnePlus 11R"],
            "Xiaomi": ["Redmi Note 13 Pro", "Xiaomi 14", "Redmi 13", "Poco X6 Pro", "Poco F6"],
            "Google": ["Pixel 8", "Pixel 8 Pro", "Pixel 8a", "Pixel 7a"],
            "Vivo": ["Vivo V30", "Vivo X100", "Vivo Y200"],
            "Oppo": ["Oppo Reno 11", "Oppo Find X7", "Oppo A79"],
            "Realme": ["Realme 12 Pro+", "Realme GT 6", "Realme Narzo 70"],
            "Motorola": ["Moto Edge 50 Pro", "Moto G84", "Moto Razr 40"],
            "Nothing": ["Nothing Phone 2", "Nothing Phone 2a"],
        },
        "low": (14999, 45000), "mult": (1.15, 1.6),
    },
    "Laptops": {
        "brands": {
            "Apple": ["MacBook Air M2", "MacBook Air M3", "MacBook Pro 14 M3", "MacBook Pro 16 M3 Pro"],
            "Dell": ["XPS 13", "XPS 15", "Inspiron 15", "Alienware m16"],
            "HP": ["Pavilion 15", "Spectre x360", "Envy 14", "Omen 16"],
            "Lenovo": ["ThinkPad X1 Carbon", "Legion 5 Pro", "IdeaPad Slim 5", "Yoga 9i"],
            "Asus": ["ROG Zephyrus G14", "Vivobook S15", "Zenbook 14 OLED", "TUF Gaming A15"],
            "Acer": ["Swift Go 14", "Predator Helios Neo 16", "Aspire 7"],
            "MSI": ["Katana 15", "Modern 14", "Stealth 16"],
        },
        "low": (42999, 90000), "mult": (1.2, 2.0),
    },
    "Tablets": {
        "brands": {
            "Apple": ["iPad 10th Gen", "iPad Air M2", "iPad Pro 11 M4", "iPad Mini 6"],
            "Samsung": ["Galaxy Tab S9", "Galaxy Tab S9 FE", "Galaxy Tab A9+"],
            "Xiaomi": ["Redmi Pad SE", "Xiaomi Pad 6"],
            "Lenovo": ["Tab P11", "Tab M10 Plus"],
            "OnePlus": ["OnePlus Pad", "OnePlus Pad Go"],
        },
        "low": (11999, 35000), "mult": (1.15, 1.7),
    },
    "Televisions": {
        "brands": {
            "Samsung": ["Crystal 4K UA43", "Neo QLED QN90D 55", "The Frame 55"],
            "LG": ["OLED C4 55", "UHD UQ7500 50", "QNED80 55"],
            "Sony": ["Bravia X75L 55", "Bravia XR A80L 55"],
            "Mi": ["Mi TV X 55", "Mi TV 5A 43"],
            "OnePlus": ["OnePlus TV Y1S 43", "OnePlus TV U1S 55"],
            "TCL": ["TCL C655 Pro 55", "TCL P745 43"],
            "Hisense": ["Hisense U6N 55", "Hisense A6K 43"],
        },
        "low": (17999, 55000), "mult": (1.2, 2.2),
    },
    "Gaming": {
        "brands": {
            "Sony": ["PlayStation 5", "PlayStation 5 Digital Edition", "PlayStation Portal", "DualSense Controller"],
            "Microsoft": ["Xbox Series X", "Xbox Series S"],
            "Nintendo": ["Nintendo Switch OLED", "Nintendo Switch Lite"],
            "Valve": ["Steam Deck OLED"],
            "Asus": ["ROG Ally"],
        },
        "low": (19999, 49999), "mult": (1.1, 1.5),
    },
    "Graphics Cards": {
        "brands": {
            "NVIDIA": ["RTX 4060", "RTX 4070 Super", "RTX 4070 Ti Super", "RTX 4080 Super", "RTX 4090"],
            "AMD": ["RX 7600", "RX 7700 XT", "RX 7800 XT", "RX 7900 XTX"],
            "Asus": ["ROG Strix RTX 4070", "TUF RX 7700 XT"],
            "MSI": ["Gaming X Trio RTX 4070 Ti", "Ventus RTX 4060"],
            "Gigabyte": ["Eagle RTX 4070", "Gaming OC RX 7800 XT"],
        },
        "low": (24999, 140000), "mult": (1.15, 1.7),
    },
    "CPUs": {
        "brands": {
            "Intel": ["Core i5-14600K", "Core i7-14700K", "Core i9-14900K", "Core i5-13400"],
            "AMD": ["Ryzen 5 7600X", "Ryzen 7 7800X3D", "Ryzen 9 7950X", "Ryzen 5 5600"],
        },
        "low": (11999, 55000), "mult": (1.1, 1.5),
    },
    "Cameras": {
        "brands": {
            "Canon": ["EOS R50", "EOS R6 Mark II", "EOS 1500D", "PowerShot G7X"],
            "Sony": ["Alpha a6400", "Alpha a7 IV", "ZV-E10"],
            "Nikon": ["Z50", "Z6 III", "D7500"],
            "Fujifilm": ["X-T30 II", "X-S20"],
            "GoPro": ["Hero 12 Black", "Hero 11 Mini"],
        },
        "low": (24999, 110000), "mult": (1.15, 1.6),
    },
    "Lenses": {
        "brands": {
            "Canon": ["RF 50mm f/1.8", "RF 24-105mm f/4L"],
            "Sony": ["FE 50mm f/1.8", "FE 24-70mm f/2.8 GM"],
            "Nikon": ["Z 35mm f/1.8", "Z 24-70mm f/4"],
            "Sigma": ["18-50mm f/2.8 Art", "56mm f/1.4 DC DN"],
            "Tamron": ["17-70mm f/2.8", "28-75mm f/2.8"],
        },
        "low": (9999, 85000), "mult": (1.15, 1.55),
    },
    "Smartwatches": {
        "brands": {
            "Apple": ["Watch SE 2nd Gen", "Watch Series 9", "Watch Ultra 2"],
            "Samsung": ["Galaxy Watch 6", "Galaxy Watch 6 Classic", "Galaxy Watch FE"],
            "Noise": ["ColorFit Pro 4", "Noise Pulse 2 Max"],
            "boAt": ["Wave Call 3", "Xtend"],
            "Fire-Boltt": ["Phoenix Pro", "Ninja Call Pro"],
            "Garmin": ["Venu 3", "Forerunner 265"],
        },
        "low": (1999, 32000), "mult": (1.1, 1.5),
    },
    "Headphones": {
        "brands": {
            "Sony": ["WH-1000XM5", "WH-CH720N"],
            "Bose": ["QuietComfort Ultra", "QuietComfort 45"],
            "JBL": ["Tune 760NC", "Live 660NC"],
            "Sennheiser": ["Momentum 4", "HD 450BT"],
            "boAt": ["Rockerz 550", "Rockerz 450 Pro"],
        },
        "low": (1499, 32000), "mult": (1.1, 1.5),
    },
    "Earbuds": {
        "brands": {
            "Apple": ["AirPods Pro 2", "AirPods 3rd Gen", "AirPods 2nd Gen"],
            "Samsung": ["Galaxy Buds2 Pro", "Galaxy Buds FE"],
            "boAt": ["Airdopes 141", "Airdopes Atom"],
            "Noise": ["Buds VS104", "Buds Prima"],
            "JBL": ["Tune 230NC", "Wave Buds"],
            "OnePlus": ["Buds 3", "Nord Buds 2"],
            "realme": ["Buds Air 5", "Buds T300"],
        },
        "low": (1299, 22000), "mult": (1.1, 1.5),
    },
    "Monitors": {
        "brands": {
            "Dell": ["S2721QS 27in 4K", "Ultrasharp U2723QE"],
            "LG": ["27GP850 QHD 165Hz", "UltraGear 27GN800"],
            "Samsung": ["Odyssey G5 27in", "M7 Smart Monitor"],
            "Asus": ["TUF Gaming VG27AQ", "ProArt PA278CV"],
            "BenQ": ["GW2780", "Mobiuz EX2710"],
            "Acer": ["Nitro XV272U", "ED270R"],
        },
        "low": (8999, 55000), "mult": (1.15, 1.6),
    },
    "Projectors": {
        "brands": {
            "Epson": ["EH-TW750", "EB-X51"],
            "BenQ": ["TH585", "TK700STi"],
            "XGIMI": ["Horizon Pro", "MoGo 2 Pro"],
            "ViewSonic": ["PX701-4K", "M1 Mini Plus"],
        },
        "low": (14999, 95000), "mult": (1.15, 1.5),
    },
    "Air Conditioners": {
        "brands": {
            "LG": ["1.5 Ton 5 Star Dual Inverter Split AC", "1 Ton 3 Star Window AC"],
            "Daikin": ["1.5 Ton 3 Star Split AC", "1 Ton 5 Star Inverter Split AC"],
            "Voltas": ["1.5 Ton 3 Star Split AC", "1 Ton 5 Star Window AC"],
            "Samsung": ["1.5 Ton WindFree Split AC", "1 Ton Convertible 5-in-1 AC"],
            "Blue Star": ["1.5 Ton 5 Star Split AC", "2 Ton 3 Star Inverter Split AC"],
            "Carrier": ["1.5 Ton 3 Star Split AC", "1 Ton 5 Star Split AC"],
        },
        "low": (28999, 65000), "mult": (1.1, 1.4),
    },
    "Refrigerators": {
        "brands": {
            "LG": ["260L Frost Free Double Door", "190L Direct Cool Single Door", "437L Side by Side"],
            "Samsung": ["236L Double Door", "580L French Door"],
            "Whirlpool": ["265L Double Door", "200L Single Door"],
            "Haier": ["258L Double Door", "192L Single Door"],
            "Godrej": ["236L Double Door", "180L Single Door"],
            "Bosch": ["347L Double Door"],
        },
        "low": (13999, 85000), "mult": (1.1, 1.4),
    },
    "Washing Machines": {
        "brands": {
            "LG": ["7Kg Front Load", "6.5Kg Top Load Fully Automatic", "9Kg Front Load"],
            "Samsung": ["7Kg Front Load with AI Wash", "6.5Kg Top Load"],
            "Bosch": ["7Kg Front Load Series 4", "8Kg Front Load Series 6"],
            "Whirlpool": ["7Kg Fully Automatic Top Load", "6.5Kg Semi Automatic"],
            "IFB": ["6.5Kg Front Load Diva Aqua", "8Kg Front Load Senator"],
            "Haier": ["7Kg Top Load Fully Automatic"],
        },
        "low": (12999, 55000), "mult": (1.1, 1.4),
    },
    "Other": {
        "brands": {
            "Amazon": ["Echo Dot 5th Gen", "Kindle Paperwhite 11th Gen", "Fire TV Stick 4K Max"],
            "Google": ["Nest Mini 2nd Gen", "Chromecast with Google TV"],
            "Xiaomi": ["Mi Smart Air Purifier 4", "Mi Robot Vacuum X10+"],
            "JBL": ["Flip 6 Portable Speaker", "Charge 5 Portable Speaker"],
            "DJI": ["Mini 4 Pro Drone", "Osmo Pocket 3"],
            "Anker": ["737 Power Bank", "PowerCore III 25W"],
            "Logitech": ["MX Master 3S Mouse", "G Pro X Superlight Mouse"],
        },
        "low": (1999, 90000), "mult": (1.1, 1.4),
    },
}

def indian_round(n):
    n = int(round(n / 100.0) * 100)
    if n > 999:
        n -= 1
    return max(n, 499)

products = []
pid = 1
combo_pool = []
for cat, info in CATALOG.items():
    for brand, models in info["brands"].items():
        for model in models:
            combo_pool.append((cat, brand, model))

random.shuffle(combo_pool)

TARGET = 500
variants = ["", " (128GB)", " (256GB)", " (Wi-Fi)", " (Wi-Fi + Cellular)", " (2024)", " (2023)", " 2nd Gen"]

i = 0
used_names = set()
while len(products) < TARGET:
    cat, brand, model = combo_pool[i % len(combo_pool)]
    variant_idx = (i // len(combo_pool)) % len(variants)
    suffix = variants[variant_idx] if variant_idx > 0 else ""
    full_name = f"{brand} {model}{suffix}"
    i += 1
    if full_name in used_names:
        continue
    used_names.add(full_name)

    info = CATALOG[cat]
    low_min, low_max = info["low"]
    mult_min, mult_max = info["mult"]

    base_low = random.uniform(low_min, low_max)
    mult = random.uniform(mult_min, mult_max)
    base_high = base_low * mult

    history = []
    cur_low, cur_high = base_low, base_high
    for m in MONTHS:
        drift_low = random.uniform(-0.04, 0.03)
        drift_high = random.uniform(-0.04, 0.03)
        cur_low = max(cur_low * (1 + drift_low), 499)
        cur_high = max(cur_high * (1 + drift_high), cur_low * 1.02)
        history.append({
            "month": m,
            "low": indian_round(cur_low),
            "high": indian_round(cur_high),
        })

    products.append({
        "id": pid,
        "brand": brand,
        "name": model + suffix,
        "category": cat,
        "model": model,
        "history": history,
    })
    pid += 1

# Writes data.js in the current root folder
with open("data.js", "w", encoding="utf-8") as f:
    f.write("// Demo historical price dataset\n")
    f.write("window.PRODUCTS = ")
    f.write(json.dumps(products, separators=(",", ":")))
    f.write(";\n")

print(f"Successfully generated data.js with {len(products)} products.")
