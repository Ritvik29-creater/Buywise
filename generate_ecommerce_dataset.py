# generate_ecommerce_dataset.py
"""
Generates a comprehensive, realistic multi-category e-commerce dataset for SmartShop Elite.
Categories:
- Electronics & Gadgets
- Computers, Laptops & Gaming
- Audio & Sound
- Home & Kitchen
- Fashion & Apparel
- Footwear & Sneakers
- Sports & Outdoors
- Beauty & Personal Care
- Gourmet & Snacks
- Books & Stationery
"""

import os
import pandas as pd

DATASET_DIR = "./dataset"
os.makedirs(DATASET_DIR, exist_ok=True)

# ── 1. DEPARTMENTS ────────────────────────────────────────────────────────────
departments_data = [
    {"department_id": 1, "department": "Electronics"},
    {"department_id": 2, "department": "Computers & Gaming"},
    {"department_id": 3, "department": "Audio & Sound"},
    {"department_id": 4, "department": "Home & Kitchen"},
    {"department_id": 5, "department": "Fashion & Apparel"},
    {"department_id": 6, "department": "Footwear"},
    {"department_id": 7, "department": "Sports & Outdoors"},
    {"department_id": 8, "department": "Beauty & Personal Care"},
    {"department_id": 9, "department": "Gourmet & Snacks"},
    {"department_id": 10, "department": "Books & Stationery"},
]
df_depts = pd.DataFrame(departments_data)
df_depts.to_csv(os.path.join(DATASET_DIR, "departments.csv"), index=False)
print("[OK] departments.csv written:", len(df_depts))

# ── 2. AISLES ─────────────────────────────────────────────────────────────────
aisles_data = [
    {"aisle_id": 101, "aisle": "Smartphones & Mobile"},
    {"aisle_id": 102, "aisle": "Tablets & E-Readers"},
    {"aisle_id": 103, "aisle": "Smartwatches & Wearables"},
    {"aisle_id": 104, "aisle": "Smart Home & Automation"},
    {"aisle_id": 201, "aisle": "Laptops & Ultrabooks"},
    {"aisle_id": 202, "aisle": "Monitors & Displays"},
    {"aisle_id": 203, "aisle": "Gaming Consoles & Peripherals"},
    {"aisle_id": 204, "aisle": "Keyboards & Mice"},
    {"aisle_id": 301, "aisle": "Noise Cancelling Headphones"},
    {"aisle_id": 302, "aisle": "Wireless Earbuds"},
    {"aisle_id": 303, "aisle": "Bluetooth Speakers"},
    {"aisle_id": 401, "aisle": "Espresso & Coffee Machines"},
    {"aisle_id": 402, "aisle": "Air Fryers & Blenders"},
    {"aisle_id": 403, "aisle": "Cookware & Chef Knives"},
    {"aisle_id": 404, "aisle": "Robot Vacuums & Cleaning"},
    {"aisle_id": 501, "aisle": "Men's Jackets & Outerwear"},
    {"aisle_id": 502, "aisle": "Hoodies & Sweatshirts"},
    {"aisle_id": 503, "aisle": "Denim & Casual Pants"},
    {"aisle_id": 504, "aisle": "Activewear & Athleisure"},
    {"aisle_id": 601, "aisle": "Running Shoes & Trainers"},
    {"aisle_id": 602, "aisle": "Lifestyle Sneakers"},
    {"aisle_id": 603, "aisle": "Boots & Casual Footwear"},
    {"aisle_id": 701, "aisle": "Fitness Trackers & Gym Gear"},
    {"aisle_id": 702, "aisle": "Yoga, Weights & Recovery"},
    {"aisle_id": 703, "aisle": "Camping & Outdoor Recreation"},
    {"aisle_id": 801, "aisle": "Skincare & Face Care"},
    {"aisle_id": 802, "aisle": "Haircare & Styling Tools"},
    {"aisle_id": 803, "aisle": "Luxury Fragrances"},
    {"aisle_id": 901, "aisle": "Protein Bars & Healthy Snacks"},
    {"aisle_id": 902, "aisle": "Specialty Coffee Beans & Tea"},
    {"aisle_id": 903, "aisle": "Sparkling Beverages & Hydration"},
    {"aisle_id": 1001, "aisle": "Bestselling Fiction & Sci-Fi"},
    {"aisle_id": 1002, "aisle": "Tech, Business & Self-Help"},
    {"aisle_id": 1003, "aisle": "Notebooks & Premium Pens"},
]
df_aisles = pd.DataFrame(aisles_data)
df_aisles.to_csv(os.path.join(DATASET_DIR, "aisles.csv"), index=False)
print("[OK] aisles.csv written:", len(df_aisles))

# ── 3. PRODUCTS ───────────────────────────────────────────────────────────────
products_data = [
    # Electronics - Smartphones (dept: 1, aisle: 101)
    {"product_id": 1, "product_name": "Apple iPhone 16 Pro Max 256GB - Natural Titanium with 48MP Camera and A18 Pro Chip", "aisle_id": 101, "department_id": 1, "price": 1199.00, "rating": 4.9, "review_count": 1840, "brand": "Apple", "description": "Flagship titanium smartphone with 48MP Fusion camera, Action Button, and next-gen A18 Pro silicon."},
    {"product_id": 2, "product_name": "Samsung Galaxy S24 Ultra 512GB - Titanium Black with S-Pen, AI Zoom, and Snapdragon 8 Gen 3", "aisle_id": 101, "department_id": 1, "price": 1299.99, "rating": 4.8, "review_count": 1420, "brand": "Samsung", "description": "Galaxy AI phone with integrated S-Pen stylus, Quad Telephoto camera, and 6.8-inch AMOLED 120Hz display."},
    {"product_id": 3, "product_name": "Google Pixel 9 Pro 128GB - Porcelain with Tensor G4 and Advanced Gemini AI Integration", "aisle_id": 101, "department_id": 1, "price": 999.00, "rating": 4.7, "review_count": 910, "brand": "Google", "description": "Clean Android flagship with triple pro camera system, Tensor G4 processor, and native Gemini AI features."},
    {"product_id": 4, "product_name": "OnePlus 12 256GB - Silky Black with 100W Fast Charging and Hasselblad Camera", "aisle_id": 101, "department_id": 1, "price": 799.99, "rating": 4.6, "review_count": 680, "brand": "OnePlus", "description": "Performance powerhouse featuring Snapdragon 8 Gen 3, 5400mAh battery, and 4th Gen Hasselblad camera."},
    {"product_id": 5, "product_name": "Anker 3-in-1 MagSafe Wireless Charging Stand with 15W Qi2 Fast Charging", "aisle_id": 101, "department_id": 1, "price": 89.99, "rating": 4.8, "review_count": 2150, "brand": "Anker", "description": "Foldable compact fast charging stand for iPhone, Apple Watch, and AirPods with certified Qi2 15W power."},

    # Electronics - Tablets (dept: 1, aisle: 102)
    {"product_id": 6, "product_name": "Apple iPad Pro 13-inch M4 OLED Ultra Retina XDR Display 256GB Space Black", "aisle_id": 102, "department_id": 1, "price": 1299.00, "rating": 4.9, "review_count": 720, "brand": "Apple", "description": "Ultra-thin tablet with breakthrough tandem OLED Ultra Retina XDR display and M4 powerhouse chip."},
    {"product_id": 7, "product_name": "Apple iPad Air 11-inch M2 Liquid Retina Display 128GB Blue", "aisle_id": 102, "department_id": 1, "price": 599.00, "rating": 4.8, "review_count": 1100, "brand": "Apple", "description": "Lightweight versatile tablet powered by M2 chip with landscape 12MP front camera and Apple Pencil Pro support."},
    {"product_id": 8, "product_name": "Amazon Kindle Paperwhite Signature Edition 32GB with Auto-Adjusting Warm Light and Wireless Charging", "aisle_id": 102, "department_id": 1, "price": 189.99, "rating": 4.8, "review_count": 4890, "brand": "Amazon", "description": "Waterproof 6.8-inch 300 ppi glare-free e-reader with weeks of battery life and wireless charging."},
    {"product_id": 9, "product_name": "Samsung Galaxy Tab S9 Ultra 14.6-inch AMOLED Display with Included S-Pen", "aisle_id": 102, "department_id": 1, "price": 1199.99, "rating": 4.7, "review_count": 540, "brand": "Samsung", "description": "Massive 14.6-inch Dynamic AMOLED 2X screen with IP68 water resistance and bundled low-latency S Pen."},

    # Electronics - Smartwatches (dept: 1, aisle: 103)
    {"product_id": 10, "product_name": "Apple Watch Ultra 2 GPS + Cellular 49mm Titanium with Black Ocean Band for Diving and Trekking", "aisle_id": 103, "department_id": 1, "price": 799.00, "rating": 4.9, "review_count": 960, "brand": "Apple", "description": "Rugged aerospace-grade titanium smartwatch with precision dual-frequency GPS and up to 72 hours battery life."},
    {"product_id": 11, "product_name": "Apple Watch Series 10 GPS 46mm Jet Black Aluminum with Midnight Sport Band", "aisle_id": 103, "department_id": 1, "price": 429.00, "rating": 4.8, "review_count": 1340, "brand": "Apple", "description": "Thinnest Apple Watch ever with larger wide-angle OLED display and sleep apnea detection."},
    {"product_id": 12, "product_name": "Garmin Fenix 7 Pro Sapphire Solar Multisport GPS Smartwatch with Flashlight and Titanium Bezel", "aisle_id": 103, "department_id": 1, "price": 799.99, "rating": 4.8, "review_count": 870, "brand": "Garmin", "description": "Ultimate outdoor endurance watch with solar charging lens, built-in LED flashlight, and topo maps."},
    {"product_id": 13, "product_name": "Samsung Galaxy Watch Ultra 47mm LTE Titanium Gray with Advanced Health & Fitness BioActive Sensor", "aisle_id": 103, "department_id": 1, "price": 649.99, "rating": 4.6, "review_count": 420, "brand": "Samsung", "description": "Durable titanium smartwatch with dual-frequency GPS, 10ATM water resistance, and Galaxy AI fitness metrics."},

    # Electronics - Smart Home (dept: 1, aisle: 104)
    {"product_id": 14, "product_name": "Philips Hue White and Color Ambiance Smart LED Starter Kit (4 A19 Bulbs + Smart Bridge)", "aisle_id": 104, "department_id": 1, "price": 199.99, "rating": 4.7, "review_count": 3210, "brand": "Philips Hue", "description": "Transform your home with 16 million colors, automated schedules, and smart home hub synchronization."},
    {"product_id": 15, "product_name": "Google Nest Learning Thermostat 4th Gen with Temperature Sensor - Polished Silver", "aisle_id": 104, "department_id": 1, "price": 279.99, "rating": 4.7, "review_count": 1150, "brand": "Google Nest", "description": "Smart thermostat with dynamic borderless display that learns your preferences and saves heating/cooling energy."},
    {"product_id": 16, "product_name": "Ring Video Doorbell Pro 2 with Head-to-Toe 1536p HD Video and 3D Motion Detection", "aisle_id": 104, "department_id": 1, "price": 249.99, "rating": 4.6, "review_count": 2760, "brand": "Ring", "description": "Premium wired doorbell with radar-powered 3D motion detection, Birds Eye View, and two-way talk."},

    # Computers - Laptops & Ultrabooks (dept: 2, aisle: 201)
    {"product_id": 17, "product_name": "Apple MacBook Pro 16-inch M3 Max Chip 36GB Unified Memory 1TB SSD Space Black", "aisle_id": 201, "department_id": 2, "price": 3499.00, "rating": 4.9, "review_count": 890, "brand": "Apple", "description": "Pro-tier laptop with Liquid Retina XDR display, up to 22 hours battery life, and thunderous M3 Max performance."},
    {"product_id": 18, "product_name": "Apple MacBook Air 15-inch M3 Chip 16GB Memory 512GB SSD Midnight", "aisle_id": 201, "department_id": 2, "price": 1499.00, "rating": 4.9, "review_count": 1650, "brand": "Apple", "description": "Incredibly slim and silent fanless laptop with vibrant 15.3-inch Liquid Retina display and 18-hour battery."},
    {"product_id": 19, "product_name": "Dell XPS 14 OLED Laptop - Intel Core Ultra 7 32GB RAM 1TB SSD RTX 4050 Platinum", "aisle_id": 201, "department_id": 2, "price": 1999.99, "rating": 4.6, "review_count": 480, "brand": "Dell", "description": "Crafted machined aluminum laptop with 3.2K OLED touch display, capacitive touch row, and dedicated RTX graphics."},
    {"product_id": 20, "product_name": "ASUS ROG Zephyrus G16 Gaming Laptop 16-inch 240Hz OLED Intel Core Ultra 9 RTX 4080 32GB RAM", "aisle_id": 201, "department_id": 2, "price": 2699.99, "rating": 4.8, "review_count": 620, "brand": "ASUS ROG", "description": "Ultra-slim gaming beast with 240Hz 2.5K OLED ROG Nebula display and GeForce RTX 4080 GPU."},
    {"product_id": 21, "product_name": "Lenovo ThinkPad X1 Carbon Gen 12 - 14-inch Ultrabook Intel Core Ultra 7 16GB RAM 512GB SSD", "aisle_id": 201, "department_id": 2, "price": 1749.00, "rating": 4.7, "review_count": 530, "brand": "Lenovo", "description": "Lightweight carbon fiber business laptop with legendary ThinkPad keyboard, robust security, and all-day endurance."},

    # Computers - Monitors & Displays (dept: 2, aisle: 202)
    {"product_id": 22, "product_name": "LG UltraGear 32-inch 4K UHD 240Hz OLED Gaming Monitor with Dual-Hz Mode and 0.03ms Response", "aisle_id": 202, "department_id": 2, "price": 1299.99, "rating": 4.8, "review_count": 710, "brand": "LG", "description": "World-class 4K OLED gaming display with dual mode (4K 240Hz or FHD 480Hz) and G-SYNC compatibility."},
    {"product_id": 23, "product_name": "Dell UltraSharp 32-inch 6K Monitor with Built-in 4K Webcam and IPS Black Technology", "aisle_id": 202, "department_id": 2, "price": 2199.99, "rating": 4.7, "review_count": 290, "brand": "Dell", "description": "Ultra-sharp 6K 6144x3456 creative workstation monitor with Thunderbolt 4 140W PD and integrated HDR webcam."},
    {"product_id": 24, "product_name": "Apple Studio Display 27-inch 5K Retina Display with Standard Glass and Tilt-Adjustable Stand", "aisle_id": 202, "department_id": 2, "price": 1599.00, "rating": 4.7, "review_count": 1120, "brand": "Apple", "description": "Breathtaking 5K Retina display with 12MP Ultra Wide camera with Center Stage, studio-quality mics, and 6 speakers."},

    # Computers - Gaming Consoles & Peripherals (dept: 2, aisle: 203)
    {"product_id": 25, "product_name": "Sony PlayStation 5 Pro Console 2TB SSD with Advanced Ray Tracing and PlayStation Spectral Super Resolution", "aisle_id": 203, "department_id": 2, "price": 699.99, "rating": 4.8, "review_count": 1450, "brand": "Sony", "description": "The most powerful PS5 console yet with upgraded GPU, PSSR AI upscaling, and 2TB high-speed NVMe storage."},
    {"product_id": 26, "product_name": "Microsoft Xbox Series X 1TB Console 4K 120FPS Gaming with Wireless Controller", "aisle_id": 203, "department_id": 2, "price": 499.99, "rating": 4.8, "review_count": 3120, "brand": "Microsoft", "description": "True 4K gaming powerhouse with 12 teraflops processing power, DirectX ray tracing, and Quick Resume."},
    {"product_id": 27, "product_name": "Valve Steam Deck OLED 512GB Handheld Gaming PC with 90Hz HDR OLED Screen", "aisle_id": 203, "department_id": 2, "price": 549.00, "rating": 4.9, "review_count": 2890, "brand": "Valve", "description": "All-in-one portable PC gaming console featuring brilliant 7.4-inch 90Hz OLED HDR display and longer battery."},
    {"product_id": 28, "product_name": "Sony DualSense Edge Wireless Controller for PS5 and PC with Customizable Back Buttons", "aisle_id": 203, "department_id": 2, "price": 199.99, "rating": 4.6, "review_count": 830, "brand": "Sony", "description": "Pro-grade modular controller with remappable back paddles, swappable stick modules, and adjustable trigger stops."},

    # Computers - Keyboards & Mice (dept: 2, aisle: 204)
    {"product_id": 29, "product_name": "Logitech MX Master 3S Wireless Performance Mouse with Quiet Clicks and 8K DPI Sensor - Graphite", "aisle_id": 204, "department_id": 2, "price": 99.99, "rating": 4.9, "review_count": 6400, "brand": "Logitech", "description": "Ergonomic productivity mouse with MagSpeed electromagnetic scroll wheel and tracking on any surface including glass."},
    {"product_id": 30, "product_name": "Logitech MX Keys S Advanced Wireless Illuminated Keyboard with Smart Backlighting", "aisle_id": 204, "department_id": 2, "price": 109.99, "rating": 4.8, "review_count": 4200, "brand": "Logitech", "description": "Low-profile precision keyboard with spherically dished keys, multi-device Bluetooth pairing, and Smart Actions."},
    {"product_id": 31, "product_name": "Keychron Q1 Pro Wireless Custom Mechanical Keyboard QMK/VIA Aluminum Gateron Jupiter Brown", "aisle_id": 204, "department_id": 2, "price": 199.99, "rating": 4.8, "review_count": 780, "brand": "Keychron", "description": "Full CNC aluminum 75% mechanical keyboard with hot-swappable switches, double-gasket design, and wireless connectivity."},

    # Audio - Noise Cancelling Headphones (dept: 3, aisle: 301)
    {"product_id": 32, "product_name": "Sony WH-1000XM5 Wireless Industry Leading Noise Canceling Headphones - Black", "aisle_id": 301, "department_id": 3, "price": 399.99, "rating": 4.8, "review_count": 5120, "brand": "Sony", "description": "Benchmark over-ear active noise cancelling headphones with dual processors, 8 microphones, and 30-hour battery life."},
    {"product_id": 33, "product_name": "Bose QuietComfort Ultra Wireless Noise Cancelling Headphones with Spatial Audio - White Smoke", "aisle_id": 301, "department_id": 3, "price": 429.00, "rating": 4.7, "review_count": 2180, "brand": "Bose", "description": "Luxurious comfort with groundbreaking spatial audio immersion, world-class noise cancellation, and CustomTune."},
    {"product_id": 34, "product_name": "Apple AirPods Max Wireless Over-Ear Headphones with Active Noise Cancellation - Space Gray", "aisle_id": 301, "department_id": 3, "price": 549.00, "rating": 4.7, "review_count": 3450, "brand": "Apple", "description": "High-fidelity audio with Apple-designed dynamic driver, computational audio with H1 chips, and breathable mesh canopy."},
    {"product_id": 35, "product_name": "Sennheiser Momentum 4 Wireless Over-Ear Headphones with 60-Hour Battery Life - Denim", "aisle_id": 301, "department_id": 3, "price": 379.95, "rating": 4.8, "review_count": 1490, "brand": "Sennheiser", "description": "Audiophile sound quality with 42mm transducer system, adaptive ANC, and unmatched 60-hour playtime."},

    # Audio - Wireless Earbuds (dept: 3, aisle: 302)
    {"product_id": 36, "product_name": "Apple AirPods Pro 2 with USB-C MagSafe Case and Hearing Health Features", "aisle_id": 302, "department_id": 3, "price": 249.00, "rating": 4.9, "review_count": 8900, "brand": "Apple", "description": "Up to 2x more Active Noise Cancellation, Adaptive Audio, Conversation Awareness, and clinical-grade Hearing Aid capability."},
    {"product_id": 37, "product_name": "Sony WF-1000XM5 Truly Wireless Noise Canceling Earbuds with High-Res Audio - Silver", "aisle_id": 302, "department_id": 3, "price": 299.99, "rating": 4.6, "review_count": 2340, "brand": "Sony", "description": "Compact premium earbuds with Dynamic Driver X, bone conduction sensors, and AI noise reduction."},
    {"product_id": 38, "product_name": "Bose QuietComfort Ultra Wireless Noise Cancelling Earbuds with Immersive Audio", "aisle_id": 302, "department_id": 3, "price": 299.00, "rating": 4.6, "review_count": 1820, "brand": "Bose", "description": "Legendary noise cancellation in a pocketable earbud format with groundbreaking spatial audio."},

    # Audio - Bluetooth Speakers (dept: 3, aisle: 303)
    {"product_id": 39, "product_name": "Sonos Move 2 Portable Smart Speaker with Bluetooth, Wi-Fi, AirPlay 2, and 24-Hour Battery - White", "aisle_id": 303, "department_id": 3, "price": 449.00, "rating": 4.8, "review_count": 1210, "brand": "Sonos", "description": "Premium weather-resistant portable speaker with expansive stereo sound, automatic Trueplay tuning, and 24-hr playback."},
    {"product_id": 40, "product_name": "JBL Flip 6 Waterproof Portable Bluetooth Speaker with 2-Way Speaker System - Ocean Blue", "aisle_id": 303, "department_id": 3, "price": 129.95, "rating": 4.8, "review_count": 7890, "brand": "JBL", "description": "IP67 waterproof and dustproof rugged outdoor speaker with punchy bass and 12 hours of playtime."},
    {"product_id": 41, "product_name": "Marshall Emberton II Portable Bluetooth Speaker with 30+ Hours of Playtime - Black and Brass", "aisle_id": 303, "department_id": 3, "price": 169.99, "rating": 4.7, "review_count": 2400, "brand": "Marshall", "description": "Iconic vintage styling with 360-degree True Stereophonic sound and IP67 rugged durability."},

    # Home & Kitchen - Coffee (dept: 4, aisle: 401)
    {"product_id": 42, "product_name": "Breville Barista Touch Impress Espresso Machine with Assisted Tamp and Auto MilQ", "aisle_id": 401, "department_id": 4, "price": 1499.95, "rating": 4.9, "review_count": 920, "brand": "Breville", "description": "Touchscreen automated espresso machine with real-time feedback, assisted 22lb tamping, and microfoam texturing."},
    {"product_id": 43, "product_name": "Nespresso VertuoPlus Coffee and Espresso Maker by De'Longhi - Matte Black", "aisle_id": 401, "department_id": 4, "price": 169.00, "rating": 4.7, "review_count": 5100, "brand": "Nespresso", "description": "Centrifusion technology brews 5 cup sizes of fresh barista-grade coffee and espresso with rich crema at the touch of a button."},
    {"product_id": 44, "product_name": "Fellow Ode Gen 2 Conical Burr Coffee Grinder with Anti-Static Technology - Matte Black", "aisle_id": 401, "department_id": 4, "price": 345.00, "rating": 4.8, "review_count": 1340, "brand": "Fellow", "description": "Precision café-grade electric burr grinder engineered specifically for filter, pour-over, and French press coffee."},

    # Home & Kitchen - Appliances (dept: 4, aisle: 402)
    {"product_id": 45, "product_name": "Ninja Foodi 6-in-1 8-qt 2-Basket Air Fryer with DualZone Technology - Dark Grey", "aisle_id": 402, "department_id": 4, "price": 199.99, "rating": 4.8, "review_count": 12400, "brand": "Ninja", "description": "Two independent baskets allow you to cook 2 foods, 2 ways, finishing at the exact same time with Smart Finish."},
    {"product_id": 46, "product_name": "Cosori TurboBlaze 6.0-Quart Air Fryer with DC Motor Technology and 9 Cooking Functions", "aisle_id": 402, "department_id": 4, "price": 119.99, "rating": 4.7, "review_count": 3890, "brand": "Cosori", "description": "Next-generation brushless DC motor delivers up to 46% faster cooking speeds with 95% less oil."},
    {"product_id": 47, "product_name": "Vitamix A3500 Ascent Series Smart Blender with 5 Program Settings and Touchscreen - Brushed Stainless", "aisle_id": 402, "department_id": 4, "price": 649.95, "rating": 4.9, "review_count": 2780, "brand": "Vitamix", "description": "Professional high-performance blender with touchscreen controls, wireless NFC Self-Detect containers, and built-in timer."},

    # Home & Kitchen - Cookware (dept: 4, aisle: 403)
    {"product_id": 48, "product_name": "All-Clad D3 Stainless Steel 10-Piece Cookware Set Tri-Ply Bonded Dishwasher Safe", "aisle_id": 403, "department_id": 4, "price": 699.99, "rating": 4.9, "review_count": 1820, "brand": "All-Clad", "description": "American-made tri-ply stainless steel cookware with responsive aluminum core for even heat distribution across all stoves."},
    {"product_id": 49, "product_name": "Le Creuset Enameled Cast Iron Signature Round Dutch Oven 5.5 qt - Cerise Red", "aisle_id": 403, "department_id": 4, "price": 420.00, "rating": 4.9, "review_count": 4120, "brand": "Le Creuset", "description": "Handcrafted French cast iron Dutch oven with vibrant enamel finish, unmatched heat retention, and lifetime durability."},
    {"product_id": 50, "product_name": "Our Place Always Pan 2.0 10.5-inch Nonstick 8-in-1 Multipurpose Frying Pan - Steam", "aisle_id": 403, "department_id": 4, "price": 150.00, "rating": 4.6, "review_count": 3100, "brand": "Our Place", "description": "Cult-favorite 8-in-1 pan that braises, sears, steams, strains, and sautés with non-toxic ceramic coating."},
    {"product_id": 51, "product_name": "Wusthof Classic 8-inch Chef's Knife Forged High-Carbon Stainless Steel", "aisle_id": 403, "department_id": 4, "price": 170.00, "rating": 4.9, "review_count": 3890, "brand": "Wusthof", "description": "Solingen Germany forged knife with full tang and triple-riveted ergonomic handle for supreme balance and precision slicing."},

    # Home & Kitchen - Robot Vacuums (dept: 4, aisle: 404)
    {"product_id": 52, "product_name": "Dyson V15 Detect Cordless Vacuum Cleaner with Laser Dust Revelation and Piezo Sensor", "aisle_id": 404, "department_id": 4, "price": 749.99, "rating": 4.8, "review_count": 3950, "brand": "Dyson", "description": "Smart cordless vacuum with laser illumination that reveals microscopic dust particles and automatically calculates suction."},
    {"product_id": 53, "product_name": "Roborock S8 Pro Ultra Robot Vacuum and Mop with RockDock Ultra Self-Washing and Drying", "aisle_id": 404, "department_id": 4, "price": 1399.99, "rating": 4.8, "review_count": 1420, "brand": "Roborock", "description": "Ultimate hands-free cleaning robot with 6000Pa suction, dual sonic vibration mopping, and auto-washing dock."},
    {"product_id": 54, "product_name": "iRobot Roomba Combo j9+ Self-Emptying & Auto-Fill Robot Vacuum and Mop", "aisle_id": 404, "department_id": 4, "price": 999.00, "rating": 4.6, "review_count": 890, "brand": "iRobot", "description": "Intelligent vacuum-mop combo with retracting mop head to prevent carpet dampness and 30-day liquid auto-fill dock."},

    # Fashion - Outerwear (dept: 5, aisle: 501)
    {"product_id": 55, "product_name": "The North Face 1996 Retro Nuptse Jacket 700-Fill Goose Down Puffer - TNF Black", "aisle_id": 501, "department_id": 5, "price": 330.00, "rating": 4.9, "review_count": 4800, "brand": "The North Face", "description": "Iconic boxy silhouette puffer jacket with water-repellent ripstop fabric and ultra-warm 700-fill responsible down."},
    {"product_id": 56, "product_name": "Arc'teryx Beta LT Jacket Men's Waterproof Breathable GORE-TEX Shell - Black", "aisle_id": 501, "department_id": 5, "price": 450.00, "rating": 4.9, "review_count": 1250, "brand": "Arc'teryx", "description": "All-mountain high performance waterproof shell jacket with 3-layer GORE-TEX fabric and storm hood."},
    {"product_id": 57, "product_name": "Patagonia Nano Puff Lightweight Water-Resistant Insulated Jacket - Forge Grey", "aisle_id": 501, "department_id": 5, "price": 239.00, "rating": 4.8, "review_count": 3120, "brand": "Patagonia", "description": "Windproof and weather-resistant midlayer with 60g PrimaLoft Gold Insulation Eco made from 100% recycled polyester."},

    # Fashion - Hoodies (dept: 5, aisle: 502)
    {"product_id": 58, "product_name": "Nike Sportswear Club Fleece Pullover Hoodie - Dark Grey Heather", "aisle_id": 502, "department_id": 5, "price": 65.00, "rating": 4.7, "review_count": 8700, "brand": "Nike", "description": "Everyday staple pullover crafted from brushed-back fleece for a soft, smooth feel and relaxed fit."},
    {"product_id": 59, "product_name": "Champion Reverse Weave Heavyweight Fleece Hoodie - Oxford Gray", "aisle_id": 502, "department_id": 5, "price": 70.00, "rating": 4.8, "review_count": 5200, "brand": "Champion", "description": "Durable heavyweight cotton fleece sweatshirt cut on the cross-grain to resist vertical shrinkage."},

    # Fashion - Pants & Denim (dept: 5, aisle: 503)
    {"product_id": 60, "product_name": "Levi's 511 Slim Fit Flex Stretch Men's Jeans - Native Cali Dark Wash", "aisle_id": 503, "department_id": 5, "price": 79.50, "rating": 4.7, "review_count": 9400, "brand": "Levi's", "description": "Modern slim-cut jeans with room to move, woven with Levi's Flex advanced stretch technology."},
    {"product_id": 61, "product_name": "Lululemon ABC Classic-Fit Pant 32L Warpstreme Fabric - Obsidian", "aisle_id": 503, "department_id": 5, "price": 128.00, "rating": 4.8, "review_count": 4300, "brand": "Lululemon", "description": "Engineered with anti-ball-crushing technology and 4-way stretch Warpstreme fabric for commute and work."},

    # Fashion - Activewear (dept: 5, aisle: 504)
    {"product_id": 62, "product_name": "Vuori Kore Short 7-inch Moisture-Wicking Athletic Shorts with Built-in Boxer Brief Liner - Charcoal", "aisle_id": 504, "department_id": 5, "price": 68.00, "rating": 4.9, "review_count": 3600, "brand": "Vuori", "description": "One short for every workout. Breathable moisture-wicking 4-way stretch fabric with anti-odor boxer brief liner."},
    {"product_id": 63, "product_name": "Gymshark Apex Seamless Breathable Gym T-Shirt - Black", "aisle_id": 504, "department_id": 5, "price": 46.00, "rating": 4.6, "review_count": 1820, "brand": "Gymshark", "description": "Heat-mapping jacquard ventilation panels with seamless stretch construction for intense lifting sessions."},
    {"product_id": 64, "product_name": "Lululemon Align High-Rise Pant 25-inch Butter-Soft Nulu Leggings - Black", "aisle_id": 504, "department_id": 5, "price": 98.00, "rating": 4.9, "review_count": 14200, "brand": "Lululemon", "description": "Weightless, buttery-soft Nulu fabric feels like a second skin for yoga, lounging, and low-impact movement."},
    {"product_id": 65, "product_name": "Nike Dri-FIT UV Miler Men's Short-Sleeve Running Top - White", "aisle_id": 504, "department_id": 5, "price": 40.00, "rating": 4.7, "review_count": 2890, "brand": "Nike", "description": "Ultralight running top with sweat-wicking technology and UVA/UVB protection in covered areas."},

    # Footwear - Running (dept: 6, aisle: 601)
    {"product_id": 66, "product_name": "Hoka Clifton 9 Lightweight Daily Running Shoes - Black / White", "aisle_id": 601, "department_id": 6, "price": 145.00, "rating": 4.8, "review_count": 6700, "brand": "Hoka", "description": "Max-cushioning daily trainer with responsive CMEVA foam, early-stage Meta-Rocker, and plush breathable engineered mesh."},
    {"product_id": 67, "product_name": "Nike Air Zoom Pegasus 41 Road Running Shoes - Platinum Tint / Green Glow", "aisle_id": 601, "department_id": 6, "price": 140.00, "rating": 4.7, "review_count": 4900, "brand": "Nike", "description": "Workhorse daily runner with ReactX foam and dual Zoom Air units for 13% more energy return."},
    {"product_id": 68, "product_name": "Brooks Ghost 16 Men's Neutral Cushion Road Running Shoes - Peacoat Blue", "aisle_id": 601, "department_id": 6, "price": 140.00, "rating": 4.8, "review_count": 5800, "brand": "Brooks", "description": "Smooth transitions and soft nitrogen-infused DNA LOFT v3 cushioning for effortless road running miles."},
    {"product_id": 69, "product_name": "On Cloudmonster Max Cushioning CloudTec Road Running Shoes - All Black", "aisle_id": 601, "department_id": 6, "price": 169.99, "rating": 4.8, "review_count": 3200, "brand": "On Running", "description": "Massive Cloud elements combined with an energetic Speedboard deliver explosive push-offs and soft landings."},

    # Footwear - Lifestyle (dept: 6, aisle: 602)
    {"product_id": 70, "product_name": "Nike Dunk Low Retro Basketball Lifestyle Sneakers - White / Black Panda", "aisle_id": 602, "department_id": 6, "price": 115.00, "rating": 4.7, "review_count": 9800, "brand": "Nike", "description": "Timeless 80s hardwood classic with crisp leather upper, padded low-cut collar, and classic contrast panels."},
    {"product_id": 71, "product_name": "New Balance 990v6 Made in USA Heritage Running Lifestyle Shoes - Castlerock Grey", "aisle_id": 602, "department_id": 6, "price": 219.99, "rating": 4.9, "review_count": 2100, "brand": "New Balance", "description": "Flagship Made in USA silhouette combining premium suede mesh uppers with FuelCell and ENCAP midsole cushioning."},
    {"product_id": 72, "product_name": "Adidas Samba OG Classic Low Top Indoor Soccer Sneakers - Cloud White / Core Black", "aisle_id": 602, "department_id": 6, "price": 100.00, "rating": 4.8, "review_count": 8400, "brand": "Adidas", "description": "Legendary street staple featuring soft full-grain leather upper, suede T-toe overlay, and gum rubber outsole."},
    {"product_id": 73, "product_name": "Salomon XT-6 Advanced Trail Running & Gorpcore Lifestyle Shoes - Vanilla Ice / Phantom", "aisle_id": 602, "department_id": 6, "price": 200.00, "rating": 4.8, "review_count": 1650, "brand": "Salomon", "description": "Technical trail shoe turned global streetwear icon with downhill chassis and Quicklace tightening system."},

    # Footwear - Boots (dept: 6, aisle: 603)
    {"product_id": 74, "product_name": "Red Wing Iron Ranger 6-inch Heritage Work Boots - Amber Harness Leather", "aisle_id": 603, "department_id": 6, "price": 349.99, "rating": 4.9, "review_count": 2400, "brand": "Red Wing", "description": "Legendary American workboot with Goodyear welt construction, double-layer leather toe cap, and Vibram 430 Mini-lug sole."},
    {"product_id": 75, "product_name": "Timberland 6-inch Premium Waterproof Leather Boots - Wheat Nubuck", "aisle_id": 603, "department_id": 6, "price": 198.00, "rating": 4.8, "review_count": 7800, "brand": "Timberland", "description": "The original waterproof yellow boot with seam-sealed construction and 400g PrimaLoft insulation."},
    {"product_id": 76, "product_name": "Blundstone 585 Classic Chelsea Boots Water-Resistant Rustic Brown Leather", "aisle_id": 603, "department_id": 6, "price": 229.95, "rating": 4.8, "review_count": 4100, "brand": "Blundstone", "description": "Iconic Australian pull-on boots with SPS Max Comfort system and durable shock-absorbing TPU outsoles."},

    # Sports - Fitness Trackers (dept: 7, aisle: 701)
    {"product_id": 77, "product_name": "WHOOP 4.0 Health, Sleep & Recovery Tracker with 12-Month Membership Included - Onyx", "aisle_id": 701, "department_id": 7, "price": 239.00, "rating": 4.6, "review_count": 1890, "brand": "WHOOP", "description": "Screenless wearable that continuously tracks strain, recovery, HRV, and sleep staging with waterproof battery pack."},
    {"product_id": 78, "product_name": "Oura Ring Gen3 Horizon Smart Ring Sleep and Heart Rate Tracker - Stealth Matte Titanium", "aisle_id": 701, "department_id": 7, "price": 399.00, "rating": 4.7, "review_count": 2340, "brand": "Oura", "description": "Titanium smart ring with research-grade biometric sensors tracking daytime heart rate, sleep scores, and Readiness."},

    # Sports - Yoga & Weights (dept: 7, aisle: 702)
    {"product_id": 79, "product_name": "Manduka PRO Yoga Mat 6mm Thick High Density Cushioning - Black Sage", "aisle_id": 702, "department_id": 7, "price": 138.00, "rating": 4.9, "review_count": 3200, "brand": "Manduka", "description": "Lifetime guarantee professional yoga mat with dense closed-cell surface that keeps sweat and bacteria out."},
    {"product_id": 80, "product_name": "Bowflex SelectTech 552 Adjustable Dumbbells Pair (5 to 52.5 lbs per dumbbell)", "aisle_id": 702, "department_id": 7, "price": 429.00, "rating": 4.8, "review_count": 8900, "brand": "Bowflex", "description": "Space-saving home gym dumbbells that replace 15 sets of weights with a turn of the adjustment dial."},
    {"product_id": 81, "product_name": "Theragun PRO Plus 6-in-1 Percussive Massage Therapy Device with Heated Therapy & Heart Rate Sensor", "aisle_id": 702, "department_id": 7, "price": 599.00, "rating": 4.8, "review_count": 1120, "brand": "Theragun", "description": "Professional recovery device combining 16mm percussive depth, near-infrared LED therapy, heat, and vibration therapy."},
    {"product_id": 82, "product_name": "Hyperice Normatec 3 Full Legs Dynamic Air Compression Recovery Boots", "aisle_id": 702, "department_id": 7, "price": 799.00, "rating": 4.9, "review_count": 910, "brand": "Hyperice", "description": "Patented biomimicry pulse technology accelerates muscle recovery and flushes metabolic waste after workouts."},

    # Sports - Outdoors (dept: 7, aisle: 703)
    {"product_id": 83, "product_name": "Hydro Flask 32 oz Wide Mouth Vacuum Insulated Stainless Steel Water Bottle with Straw Lid - Pacific", "aisle_id": 703, "department_id": 7, "price": 44.95, "rating": 4.9, "review_count": 11500, "brand": "Hydro Flask", "description": "TempShield double-wall vacuum insulation keeps ice cold for up to 24 hours with leakproof flex straw cap."},
    {"product_id": 84, "product_name": "YETI Tundra 45 Hard Cooler Heavy Duty Rotomolded Ice Chest - Desert Tan", "aisle_id": 703, "department_id": 7, "price": 325.00, "rating": 4.9, "review_count": 4800, "brand": "YETI", "description": "Indestructible rotomolded construction with PermaFrost 3-inch pressure-injected polyurethane insulation walls."},
    {"product_id": 85, "product_name": "MSR Hubba Hubba 2-Person Lightweight Backpacking Tent with DuraShield Waterproof Coating", "aisle_id": 703, "department_id": 7, "price": 479.95, "rating": 4.8, "review_count": 890, "brand": "MSR", "description": "Ultra-reliable 3-season free-standing backpacking tent weighing under 3 lbs with Easton Syclone poles."},

    # Beauty - Skincare (dept: 8, aisle: 801)
    {"product_id": 86, "product_name": "The Ordinary Niacinamide 10% + Zinc 1% Oil Control & Blemish Reduction Face Serum 60ml", "aisle_id": 801, "department_id": 8, "price": 10.80, "rating": 4.7, "review_count": 18400, "brand": "The Ordinary", "description": "Water-based vitamin and mineral formula that visibly smooths skin texture and reduces sebum activity."},
    {"product_id": 87, "product_name": "CeraVe Hydrating Facial Cleanser with Essential Ceramides and Hyaluronic Acid 16 oz", "aisle_id": 801, "department_id": 8, "price": 16.99, "rating": 4.8, "review_count": 24200, "brand": "CeraVe", "description": "Gentle non-foaming lotion cleanser developed with dermatologists to restore the natural skin barrier."},
    {"product_id": 88, "product_name": "Paula's Choice Skin Perfecting 2% BHA Liquid Salicylic Acid Exfoliant 4 oz", "aisle_id": 801, "department_id": 8, "price": 35.00, "rating": 4.8, "review_count": 15600, "brand": "Paula's Choice", "description": "Global bestseller leave-on exfoliant that unclogs enlarged pores, smooths wrinkles, and brightens tone."},
    {"product_id": 89, "product_name": "La Roche-Posay Anthelios Ultra-Light Fluid Sunscreen SPF 60 with Cell-Ox Shield", "aisle_id": 801, "department_id": 8, "price": 33.99, "rating": 4.8, "review_count": 8900, "brand": "La Roche-Posay", "description": "Fast-absorbing matte sunscreen with broad spectrum UVA/UVB protection and advanced antioxidant defenses."},

    # Beauty - Haircare (dept: 8, aisle: 802)
    {"product_id": 90, "product_name": "Dyson Airwrap Multi-Styler Complete Long Hair Styling Tool - Nickel and Copper", "aisle_id": 802, "department_id": 8, "price": 599.99, "rating": 4.8, "review_count": 4200, "brand": "Dyson", "description": "Harnesses the aerodynamic Coanda effect to curl, wave, smooth, and dry hair with no extreme heat damage."},
    {"product_id": 91, "product_name": "Olaplex No. 3 Hair Perfector Repairing Treatment for Damaged Hair 3.3 fl oz", "aisle_id": 802, "department_id": 8, "price": 30.00, "rating": 4.7, "review_count": 16800, "brand": "Olaplex", "description": "At-home pre-shampoo hair treatment proven to repair broken disulfide bonds and reduce breakage."},
    {"product_id": 92, "product_name": "Moroccanoil Treatment Original Argan Oil Hair Treatment & Styling Elixir 3.4 oz", "aisle_id": 802, "department_id": 8, "price": 48.00, "rating": 4.9, "review_count": 9200, "brand": "Moroccanoil", "description": "Argan-oil infused nourishing hair treatment that conditions, detangles, and speeds up blow-drying time."},

    # Beauty - Fragrances (dept: 8, aisle: 803)
    {"product_id": 93, "product_name": "Bleu de Chanel Eau de Parfum Spray 100ml / 3.4 oz Woody Aromatic Fragrance", "aisle_id": 803, "department_id": 8, "price": 165.00, "rating": 4.9, "review_count": 5600, "brand": "Chanel", "description": "Timeless masculine scent featuring fresh citrus top notes over ambery cedar and New Caledonian sandalwood."},
    {"product_id": 94, "product_name": "Dior Sauvage Eau de Parfum 100ml / 3.4 oz Fresh Spicy Bergamot & Amber Vanilla", "aisle_id": 803, "department_id": 8, "price": 160.00, "rating": 4.8, "review_count": 6800, "brand": "Dior", "description": "Radically fresh composition with radiant Calabrian bergamot and a powerfully sensual Papua New Guinean vanilla trail."},
    {"product_id": 95, "product_name": "Tom Ford Tobacco Vanille Eau de Parfum 50ml Warm Spicy Gourmand Luxury Fragrance", "aisle_id": 803, "department_id": 8, "price": 295.00, "rating": 4.9, "review_count": 2100, "brand": "Tom Ford", "description": "Opulent artisanal scent reminiscent of an English gentleman's club with aromatic spices, tobacco leaf, and vanilla."},
    {"product_id": 96, "product_name": "Maison Francis Kurkdjian Baccarat Rouge 540 Eau de Parfum 70ml Floral Amber Wood", "aisle_id": 803, "department_id": 8, "price": 325.00, "rating": 4.9, "review_count": 3400, "brand": "MFK", "description": "Luminous olfactory alchemy with breezy jasmine nuances, radiant saffron, ambergris minerals, and freshly cut cedar."},

    # Gourmet - Snacks (dept: 9, aisle: 901)
    {"product_id": 97, "product_name": "RXBAR High Protein Snack Bars Variety Pack (Chocolate Sea Salt, Peanut Butter, Blueberry) 12 Pack", "aisle_id": 901, "department_id": 9, "price": 27.99, "rating": 4.7, "review_count": 8900, "brand": "RXBAR", "description": "Clean protein bars made with egg whites, dates, and nuts. 12g protein with zero added sugars."},
    {"product_id": 98, "product_name": "Barebells Delicious Protein Bars Low Sugar 20g Protein - Creamy Crisp (12 Pack)", "aisle_id": 901, "department_id": 9, "price": 29.99, "rating": 4.9, "review_count": 4600, "brand": "Barebells", "description": "Candy bar taste without the guilt. 20 grams of high quality protein and only 1 gram of sugar per bar."},
    {"product_id": 99, "product_name": "KIND Dark Chocolate Nuts & Sea Salt Healthy Gluten-Free Snack Bars (12 Pack)", "aisle_id": 901, "department_id": 9, "price": 18.99, "rating": 4.8, "review_count": 12100, "brand": "KIND", "description": "Whole almonds, crunchy peanuts, and dark chocolate drizzle with only 5g sugar and no artificial sweeteners."},
    {"product_id": 100, "product_name": "Organic Dried Turkish Mango Slices - Non-GMO Sulphur-Free Dried Fruit 16 oz", "aisle_id": 901, "department_id": 9, "price": 15.99, "rating": 4.8, "review_count": 2300, "brand": "Terra Organic", "description": "Sun-ripened organic mango slices with chewy texture and sweet tropical flavor, completely unsweetened."},

    # Gourmet - Coffee & Tea (dept: 9, aisle: 902)
    {"product_id": 101, "product_name": "Blue Bottle Coffee Giant Steps Whole Bean Coffee 12 oz Dark Roast with Cocoa & Marshmallow Notes", "aisle_id": 902, "department_id": 9, "price": 21.00, "rating": 4.8, "review_count": 2890, "brand": "Blue Bottle", "description": "Viscous full-bodied dark roast blend ideal for French press, drip, or espresso with milk."},
    {"product_id": 102, "product_name": "Stumptown Coffee Roasters Hair Bender Whole Bean Coffee 12 oz Complex Citrus & Chocolate Blend", "aisle_id": 902, "department_id": 9, "price": 19.99, "rating": 4.8, "review_count": 3120, "brand": "Stumptown", "description": "Historic espresso and drip blend with sweet toffee, rich milk chocolate, and cherry brightness."},
    {"product_id": 103, "product_name": "Ippodo Tea Japanese Ceremonial Grade Sayaka-no-Mukashi Matcha Powder 40g Tin", "aisle_id": 902, "department_id": 9, "price": 38.00, "rating": 4.9, "review_count": 1400, "brand": "Ippodo Tea", "description": "Kyoto ceremonial grade Uji matcha with vibrant jade color, umami richness, and zero bitterness."},

    # Gourmet - Beverages (dept: 9, aisle: 903)
    {"product_id": 104, "product_name": "San Pellegrino Sparkling Natural Mineral Water Glass Bottles 750ml (12 Pack)", "aisle_id": 903, "department_id": 9, "price": 32.99, "rating": 4.9, "review_count": 6700, "brand": "San Pellegrino", "description": "Italian sparkling mineral water bottled at the source in the Italian Alps with crisp carbonation."},
    {"product_id": 105, "product_name": "Poppi Sparkling Prebiotic Soda Variety Pack - Gut Healthy Low Sugar Soda (12 Pack)", "aisle_id": 903, "department_id": 9, "price": 29.88, "rating": 4.7, "review_count": 4890, "brand": "Poppi", "description": "Modern soda infused with organic apple cider vinegar and prebiotics. 5g sugar and 25 calories."},
    {"product_id": 106, "product_name": "Liquid Death Mountain Water in Infinitely Recyclable Tallboy Cans 16.9 oz (12 Pack)", "aisle_id": 903, "department_id": 9, "price": 16.99, "rating": 4.8, "review_count": 8900, "brand": "Liquid Death", "description": "Pure Austrian Alps mountain spring water canned directly at the source in ice-cold tallboy cans."},

    # Books - Fiction (dept: 10, aisle: 1001)
    {"product_id": 107, "product_name": "Project Hail Mary by Andy Weir - Hardcover Sci-Fi Survival Novel", "aisle_id": 1001, "department_id": 10, "price": 28.00, "rating": 4.9, "review_count": 32000, "brand": "Del Rey Books", "description": "Interstellar survival masterpiece from the author of The Martian. A lone astronaut must save Earth."},
    {"product_id": 108, "product_name": "Dune by Frank Herbert - Deluxe Hardcover Classic Science Fiction Epic", "aisle_id": 1001, "department_id": 10, "price": 35.00, "rating": 4.9, "review_count": 28500, "brand": "Ace Books", "description": "The greatest sci-fi epic of all time featuring painted edges, custom endpapers, and full-color map."},
    {"product_id": 109, "product_name": "Tomorrow, and Tomorrow, and Tomorrow by Gabrielle Zevin - Bestselling Hardcover Novel", "aisle_id": 1001, "department_id": 10, "price": 28.00, "rating": 4.7, "review_count": 19400, "brand": "Knopf", "description": "Multi-decade romance and creative partnership between video game designers. New York Times Bestseller."},

    # Books - Business & Tech (dept: 10, aisle: 1002)
    {"product_id": 110, "product_name": "Atomic Habits: An Easy & Proven Way to Build Good Habits by James Clear - Hardcover", "aisle_id": 1002, "department_id": 10, "price": 27.00, "rating": 4.9, "review_count": 94000, "brand": "Avery Publishing", "description": "The definitive guide to breaking bad behaviors and adopting good habits through 1% daily compounding."},
    {"product_id": 111, "product_name": "Designing Data-Intensive Applications: The Big Ideas Behind Reliable Distributed Systems by Martin Kleppmann", "aisle_id": 1002, "department_id": 10, "price": 49.99, "rating": 4.9, "review_count": 7800, "brand": "O'Reilly Media", "description": "The quintessential architecture reference for distributed databases, transactions, and stream processing."},
    {"product_id": 112, "product_name": "Thinking, Fast and Slow by Daniel Kahneman - International Bestselling Psychology Paperback", "aisle_id": 1002, "department_id": 10, "price": 18.00, "rating": 4.8, "review_count": 42000, "brand": "Farrar, Straus and Giroux", "description": "Nobel laureate analysis of System 1 and System 2 human cognitive biases, heuristics, and judgment."},
    {"product_id": 113, "product_name": "Deep Work: Rules for Focused Success in a Distracted World by Cal Newport - Hardcover", "aisle_id": 1002, "department_id": 10, "price": 28.00, "rating": 4.8, "review_count": 16500, "brand": "Grand Central Publishing", "description": "Transformative guide for achieving superhuman focus, cognitive depth, and elite productivity."},

    # Books - Stationery (dept: 10, aisle: 1003)
    {"product_id": 114, "product_name": "Leuchtturm1917 Hardcover Medium A5 Dotted Bullet Journal Notebook - Emerald Green", "aisle_id": 1003, "department_id": 10, "price": 25.50, "rating": 4.8, "review_count": 8200, "brand": "Leuchtturm1917", "description": "Ink-proof 80gsm paper, numbered pages, table of contents, dual page markers, and expandable back pocket."},
    {"product_id": 115, "product_name": "Lamy 2000 Makrolon Fiberglass Piston-Fill Fountain Pen with 14K Gold Nib", "aisle_id": 1003, "department_id": 10, "price": 220.00, "rating": 4.9, "review_count": 1850, "brand": "Lamy", "description": "Bauhaus design icon made of seamless brushed Makrolon fiberglass with platinum-coated 14-karat gold nib."},
    {"product_id": 116, "product_name": "Pilot G2 0.7mm Premium Retractable Gel Roller Pens - Black Ink (Pack of 12)", "aisle_id": 1003, "department_id": 10, "price": 14.99, "rating": 4.8, "review_count": 31000, "brand": "Pilot", "description": "Longest-writing gel ink pens with comfortable contoured rubber grip and vibrant, skip-free black ink."},
]
df_products = pd.DataFrame(products_data)
df_products.to_csv(os.path.join(DATASET_DIR, "products.csv"), index=False)
print("[OK] products.csv written:", len(df_products))

# ── 4. ORDERS & PRIOR PURCHASES ───────────────────────────────────────────────
orders_data = [
    # User 1: Tech enthusiast & coffee lover
    {"order_id": 101, "user_id": 1, "order_number": 1, "order_dow": 1, "order_hour_of_day": 10, "days_since_prior_order": 0},
    {"order_id": 102, "user_id": 1, "order_number": 2, "order_dow": 2, "order_hour_of_day": 14, "days_since_prior_order": 5},
    {"order_id": 103, "user_id": 1, "order_number": 3, "order_dow": 5, "order_hour_of_day": 11, "days_since_prior_order": 7},
    {"order_id": 104, "user_id": 1, "order_number": 4, "order_dow": 0, "order_hour_of_day": 16, "days_since_prior_order": 12},

    # User 2: Runner & Fitness enthusiast
    {"order_id": 201, "user_id": 2, "order_number": 1, "order_dow": 3, "order_hour_of_day": 9, "days_since_prior_order": 0},
    {"order_id": 202, "user_id": 2, "order_number": 2, "order_dow": 6, "order_hour_of_day": 12, "days_since_prior_order": 14},
    {"order_id": 203, "user_id": 2, "order_number": 3, "order_dow": 1, "order_hour_of_day": 18, "days_since_prior_order": 6},

    # User 3: Home & Chef gourmet
    {"order_id": 301, "user_id": 3, "order_number": 1, "order_dow": 2, "order_hour_of_day": 15, "days_since_prior_order": 0},
    {"order_id": 302, "user_id": 3, "order_number": 2, "order_dow": 4, "order_hour_of_day": 13, "days_since_prior_order": 10},

    # User 4: Student & Developer
    {"order_id": 401, "user_id": 4, "order_number": 1, "order_dow": 0, "order_hour_of_day": 20, "days_since_prior_order": 0},
    {"order_id": 402, "user_id": 4, "order_number": 2, "order_dow": 3, "order_hour_of_day": 17, "days_since_prior_order": 8},

    # User 5: Fashion & Beauty enthusiast
    {"order_id": 501, "user_id": 5, "order_number": 1, "order_dow": 6, "order_hour_of_day": 19, "days_since_prior_order": 0},
    {"order_id": 502, "user_id": 5, "order_number": 2, "order_dow": 4, "order_hour_of_day": 14, "days_since_prior_order": 9},
]
df_orders = pd.DataFrame(orders_data)
df_orders.to_csv(os.path.join(DATASET_DIR, "orders.csv"), index=False)
print("[OK] orders.csv written:", len(df_orders))

# ── 5. PRIOR ORDER PRODUCTS ───────────────────────────────────────────────────
prior_data = [
    # Order 101: MacBook Pro setup
    {"order_id": 101, "product_id": 17, "add_to_cart_order": 1, "reordered": 0}, # MacBook Pro
    {"order_id": 101, "product_id": 29, "add_to_cart_order": 2, "reordered": 0}, # MX Master 3S
    {"order_id": 101, "product_id": 32, "add_to_cart_order": 3, "reordered": 0}, # Sony WH-1000XM5

    # Order 102: Morning Coffee essentials
    {"order_id": 102, "product_id": 43, "add_to_cart_order": 1, "reordered": 0}, # Nespresso
    {"order_id": 102, "product_id": 101, "add_to_cart_order": 2, "reordered": 0}, # Blue Bottle coffee

    # Order 103: Phone upgrade & snacks
    {"order_id": 103, "product_id": 1, "add_to_cart_order": 1, "reordered": 0},  # iPhone 16 Pro Max
    {"order_id": 103, "product_id": 5, "add_to_cart_order": 2, "reordered": 0},  # Anker MagSafe
    {"order_id": 103, "product_id": 101, "add_to_cart_order": 3, "reordered": 1}, # Blue Bottle coffee (reordered)
    {"order_id": 103, "product_id": 97, "add_to_cart_order": 4, "reordered": 0},  # RXBAR

    # Order 104: Reading & Desk
    {"order_id": 104, "product_id": 110, "add_to_cart_order": 1, "reordered": 0}, # Atomic Habits
    {"order_id": 104, "product_id": 114, "add_to_cart_order": 2, "reordered": 0}, # Leuchtturm Notebook
    {"order_id": 104, "product_id": 116, "add_to_cart_order": 3, "reordered": 0}, # Pilot G2 Pens

    # Order 201: Running Gear
    {"order_id": 201, "product_id": 67, "add_to_cart_order": 1, "reordered": 0}, # Nike Pegasus
    {"order_id": 201, "product_id": 12, "add_to_cart_order": 2, "reordered": 0}, # Garmin Fenix 7
    {"order_id": 201, "product_id": 83, "add_to_cart_order": 3, "reordered": 0}, # Hydro Flask

    # Order 202: Recovery & Supplements
    {"order_id": 202, "product_id": 81, "add_to_cart_order": 1, "reordered": 0}, # Theragun Pro
    {"order_id": 202, "product_id": 98, "add_to_cart_order": 2, "reordered": 0}, # Barebells Protein Bars
    {"order_id": 202, "product_id": 106, "add_to_cart_order": 3, "reordered": 0}, # Liquid Death Water

    # Order 203: Trail running
    {"order_id": 203, "product_id": 69, "add_to_cart_order": 1, "reordered": 0}, # On Cloudmonster
    {"order_id": 203, "product_id": 65, "add_to_cart_order": 2, "reordered": 0}, # Nike Dri-FIT
    {"order_id": 203, "product_id": 98, "add_to_cart_order": 3, "reordered": 1}, # Barebells (reordered)

    # Order 301: Kitchen upgrade
    {"order_id": 301, "product_id": 42, "add_to_cart_order": 1, "reordered": 0}, # Breville Barista
    {"order_id": 301, "product_id": 49, "add_to_cart_order": 2, "reordered": 0}, # Le Creuset Dutch Oven
    {"order_id": 301, "product_id": 51, "add_to_cart_order": 3, "reordered": 0}, # Wusthof Knife

    # Order 302: Blending & Cleaning
    {"order_id": 302, "product_id": 47, "add_to_cart_order": 1, "reordered": 0}, # Vitamix Blender
    {"order_id": 302, "product_id": 52, "add_to_cart_order": 2, "reordered": 0}, # Dyson V15 Vacuum

    # Order 401: Developer setup
    {"order_id": 401, "product_id": 22, "add_to_cart_order": 1, "reordered": 0}, # LG OLED Monitor
    {"order_id": 401, "product_id": 31, "add_to_cart_order": 2, "reordered": 0}, # Keychron Q1 Keyboard
    {"order_id": 401, "product_id": 111, "add_to_cart_order": 3, "reordered": 0}, # Designing Data-Intensive Apps

    # Order 402: Audio upgrade
    {"order_id": 402, "product_id": 36, "add_to_cart_order": 1, "reordered": 0}, # AirPods Pro 2
    {"order_id": 402, "product_id": 58, "add_to_cart_order": 2, "reordered": 0}, # Nike Club Fleece Hoodie

    # Order 501: Skincare & Fragrance
    {"order_id": 501, "product_id": 86, "add_to_cart_order": 1, "reordered": 0}, # The Ordinary Niacinamide
    {"order_id": 501, "product_id": 87, "add_to_cart_order": 2, "reordered": 0}, # CeraVe Cleanser
    {"order_id": 501, "product_id": 93, "add_to_cart_order": 3, "reordered": 0}, # Bleu de Chanel

    # Order 502: Luxury haircare
    {"order_id": 502, "product_id": 90, "add_to_cart_order": 1, "reordered": 0}, # Dyson Airwrap
    {"order_id": 502, "product_id": 91, "add_to_cart_order": 2, "reordered": 0}, # Olaplex No. 3
    {"order_id": 502, "product_id": 64, "add_to_cart_order": 3, "reordered": 0}, # Lululemon Align Leggings
]
df_prior = pd.DataFrame(prior_data)
df_prior.to_csv(os.path.join(DATASET_DIR, "order_products__prior.csv"), index=False)
print("[OK] order_products__prior.csv written:", len(df_prior))

print("\n[OK] Complete e-commerce dataset generated successfully!")
