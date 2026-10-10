import os
import random
import pandas as pd

DATASET_DIR = "./dataset"
os.makedirs(DATASET_DIR, exist_ok=True)

PRODUCTS = [
    # ══════════════════════════════════════════════════════════════════════════
    # 1. ELECTRONICS & MOBILE (Dept 1)
    # ══════════════════════════════════════════════════════════════════════════
    # Aisle 101: Smartphones & Mobile Devices
    {
        "product_id": 1,
        "product_name": "Apple iPhone 16 Pro Max 256GB - Natural Titanium with 48MP Camera & A18 Pro Chip",
        "aisle_id": 101, "department_id": 1, "price": 1199.00, "rating": 4.9, "review_count": 1840,
        "brand": "Apple",
        "description": "Grade 5 titanium aerospace design, 6.9-inch Super Retina XDR OLED 120Hz ProMotion display, Camera Control button, 48MP Fusion sensor with 5x optical telephoto, A18 Pro 3nm chipset with Apple Intelligence, 33-hour battery life, USB-C 3.2 Gen 2 (10Gbps)."
    },
    {
        "product_id": 2,
        "product_name": "Samsung Galaxy S24 Ultra 512GB - Titanium Black with Built-in S Pen & Galaxy AI",
        "aisle_id": 101, "department_id": 1, "price": 1299.99, "rating": 4.8, "review_count": 1420,
        "brand": "Samsung",
        "description": "6.8-inch Dynamic AMOLED 2X 120Hz flat display with anti-reflective Corning Gorilla Armor, integrated S Pen stylus, Snapdragon 8 Gen 3 for Galaxy, 200MP wide sensor with Quad Telephoto system (5x & 10x optical quality), 5000mAh battery with 45W fast charge, 7 years OS updates."
    },
    {
        "product_id": 3,
        "product_name": "Google Pixel 9 Pro XL 256GB - Hazel with Tensor G4 & Gemini Nano AI",
        "aisle_id": 101, "department_id": 1, "price": 1099.00, "rating": 4.7, "review_count": 910,
        "brand": "Google",
        "description": "6.8-inch Super Actua LTPO OLED 3000 nits peak brightness, Google Tensor G4 with 16GB RAM for on-device Gemini AI, pro triple rear camera system with 50MP main and 48MP 5x telephoto, 42MP autofocus selfie camera, satellite SOS, 7 years feature drops and OS updates."
    },
    {
        "product_id": 4,
        "product_name": "OnePlus 12 256GB - Silky Black with 100W SuperVOOC Fast Charging & Hasselblad Camera",
        "aisle_id": 101, "department_id": 1, "price": 799.99, "rating": 4.6, "review_count": 680,
        "brand": "OnePlus",
        "description": "Snapdragon 8 Gen 3 flagship with Dual Cryo-velocity VC cooling, 5400mAh dual-cell battery with 80W US / 100W global fast charging and 50W wireless AIRVOOC, 6.82-inch 2K ProXDR 120Hz display, 4th Gen Hasselblad camera with 64MP 3x periscope zoom."
    },
    {
        "product_id": 5,
        "product_name": "Apple iPhone 16 128GB - Ultramarine with A18 Chip & Camera Control",
        "aisle_id": 101, "department_id": 1, "price": 799.00, "rating": 4.8, "review_count": 1150,
        "brand": "Apple",
        "description": "Color-infused back glass with aerospace-grade aluminum, Action Button, Camera Control, 48MP 2-in-1 Fusion camera with 2x optical-quality telephoto, spatial photo/video capture for Apple Vision Pro, A18 3nm silicon, Ceramic Shield front."
    },
    {
        "product_id": 6,
        "product_name": "Google Pixel 8a 128GB - Bay Blue with Tensor G3 & Best Take AI",
        "aisle_id": 101, "department_id": 1, "price": 499.00, "rating": 4.6, "review_count": 890,
        "brand": "Google",
        "description": "Mid-range champion featuring Google Tensor G3, 6.1-inch Actua 120Hz OLED screen, 64MP dual camera with Magic Eraser and Best Take, IP67 water/dust resistance, all-day 24h battery life, and 7 years of Android OS and security updates."
    },
    {
        "product_id": 7,
        "product_name": "Samsung Galaxy Z Fold 6 512GB - Silver Shadow with S Pen Support & Dual Screen",
        "aisle_id": 101, "department_id": 1, "price": 1899.99, "rating": 4.6, "review_count": 520,
        "brand": "Samsung",
        "description": "Ultra-slim book-style foldable with 7.6-inch Dynamic AMOLED 2X 2600 nits inner screen and 6.3-inch outer cover screen, Armor Aluminum frame, Snapdragon 8 Gen 3, IP48 water resistance, multitasking Flex Mode, and Note Assist AI."
    },
    {
        "product_id": 8,
        "product_name": "Samsung Galaxy Z Flip 6 256GB - Mint with 3.4-inch Flex Window & 50MP Camera",
        "aisle_id": 101, "department_id": 1, "price": 1099.99, "rating": 4.7, "review_count": 640,
        "brand": "Samsung",
        "description": "Compact clamshell folding phone featuring 3.4-inch Super AMOLED FlexWindow cover display with widget controls, 50MP main sensor with FlexCam auto zoom, 4000mAh battery with vapor chamber cooling, and Armor Aluminum hinge."
    },
    {
        "product_id": 9,
        "product_name": "Motorola Razr+ 2024 256GB - Midnight Blue with 4.0-inch Full-Function External OLED",
        "aisle_id": 101, "department_id": 1, "price": 899.99, "rating": 4.5, "review_count": 310,
        "brand": "Motorola",
        "description": "Flip smartphone featuring massive 4.0-inch 165Hz pOLED cover display capable of running any full app, Snapdragon 8s Gen 3, 50MP telephoto zoom, vegan leather finish, IPX8 underwater protection, and 45W TurboPower charging."
    },
    {
        "product_id": 10,
        "product_name": "Sony Xperia 1 VI 256GB - Platinum Silver with True Optical Continuous Zoom 85-170mm",
        "aisle_id": 101, "department_id": 1, "price": 1399.00, "rating": 4.5, "review_count": 210,
        "brand": "Sony",
        "description": "Audiophile and creator phone featuring 3.5mm headphone jack, dedicated two-stage camera shutter button, 85-170mm true continuous optical telephoto zoom, telephoto macro mode, Bravia-tuned OLED 120Hz display, and 2-day battery life."
    },

    # Aisle 102: Tablets & E-Readers
    {
        "product_id": 11,
        "product_name": "Apple iPad Pro 13-inch M4 OLED Ultra Retina XDR 256GB Space Black",
        "aisle_id": 102, "department_id": 1, "price": 1299.00, "rating": 4.9, "review_count": 720,
        "brand": "Apple",
        "description": "5.1mm ultra-thin chassis, Tandem OLED Ultra Retina XDR display with 1600 nits peak HDR brightness and 2,000,000:1 contrast ratio, M4 10-core GPU chip with hardware-accelerated ray tracing, Apple Pencil Pro barrel roll and haptic support, Thunderbolt / USB 4."
    },
    {
        "product_id": 12,
        "product_name": "Apple iPad Air 11-inch M2 Liquid Retina Display 128GB Starlight",
        "aisle_id": 102, "department_id": 1, "price": 599.00, "rating": 4.8, "review_count": 1100,
        "brand": "Apple",
        "description": "High-versatility tablet driven by Apple M2 silicon, 11-inch Liquid Retina True Tone P3 wide color display, landscape 12MP Center Stage front camera, Touch ID top button, Wi-Fi 6E, compatible with Magic Keyboard and Apple Pencil Pro."
    },
    {
        "product_id": 13,
        "product_name": "Amazon Kindle Paperwhite Signature Edition 32GB Waterproof with Auto-Light",
        "aisle_id": 102, "department_id": 1, "price": 189.99, "rating": 4.8, "review_count": 4890,
        "brand": "Amazon",
        "description": "6.8-inch 300 ppi glare-free e-ink screen, auto-adjusting warm light for night reading, IPX8 waterproof rating for beach and bathtub reading, Qi wireless charging, up to 10 weeks battery life on single USB-C charge, 32GB storage for thousands of audiobooks and books."
    },
    {
        "product_id": 14,
        "product_name": "Samsung Galaxy Tab S9 Ultra 14.6-inch Dynamic AMOLED 2X 256GB with S-Pen",
        "aisle_id": 102, "department_id": 1, "price": 1199.99, "rating": 4.7, "review_count": 540,
        "brand": "Samsung",
        "description": "Massive 14.6-inch Dynamic AMOLED 2X 120Hz display with Vision Booster, IP68 water/dust resistance for tablet and bundled low-latency S Pen, Snapdragon 8 Gen 2 for Galaxy, Samsung DeX desktop computing mode, quad AKG Dolby Atmos speakers."
    },
    {
        "product_id": 15,
        "product_name": "reMarkable 2 Digital Paper E-Ink Tablet with Marker Plus and Folio",
        "aisle_id": 102, "department_id": 1, "price": 449.00, "rating": 4.7, "review_count": 1340,
        "brand": "reMarkable",
        "description": "Distraction-free digital notebook with 10.3-inch monochrome CANVAS paper display, ultra-low latency writing experience mimicking real pen on textured paper, 4.7mm thickness, PDF annotation, handwriting-to-text conversion, 2-week battery life."
    },

    # Aisle 103: Smartwatches & Wearables
    {
        "product_id": 16,
        "product_name": "Apple Watch Ultra 2 49mm Titanium GPS+Cellular with Sapphire Crystal & Depth Gauge",
        "aisle_id": 103, "department_id": 1, "price": 799.00, "rating": 4.9, "review_count": 2100,
        "brand": "Apple",
        "description": "Aerospace titanium 49mm case, 3000-nit flat sapphire display, S9 SiP with Double Tap gesture, precision dual-frequency GPS (L1 and L5), 100m water resistance with EN13319 dive computer certification and depth gauge, 36-hour normal / 72-hour low power battery life, 86dB emergency siren."
    },
    {
        "product_id": 17,
        "product_name": "Apple Watch Series 10 46mm Jet Black Aluminum with ECG & Sleep Apnea Detection",
        "aisle_id": 103, "department_id": 1, "price": 429.00, "rating": 4.8, "review_count": 1650,
        "brand": "Apple",
        "description": "Thinnest Apple Watch ever with 40% brighter wide-angle OLED display, S10 SiP chip, sleep apnea notifications, ECG app, blood oxygen sensing, wrist temperature tracking, water depth to 6 meters, fast charging to 80% in 30 minutes."
    },
    {
        "product_id": 18,
        "product_name": "Garmin Fenix 8 AMOLED 51mm Multi-Sport GPS Smartwatch with Diving & Mic",
        "aisle_id": 103, "department_id": 1, "price": 1099.99, "rating": 4.9, "review_count": 890,
        "brand": "Garmin",
        "description": "Premium multi-sport watch with 1.4-inch vibrant AMOLED display, titanium bezel, leakproof inductive buttons, 40-meter dive rating, built-in speaker and mic for voice commands, LED flashlight, TopoActive multi-continent maps, up to 29 days battery life in smartwatch mode."
    },
    {
        "product_id": 19,
        "product_name": "Samsung Galaxy Watch Ultra 47mm Titanium Grey with Dual-Frequency GPS & BioActive Sensor",
        "aisle_id": 103, "department_id": 1, "price": 649.99, "rating": 4.7, "review_count": 780,
        "brand": "Samsung",
        "description": "Rugged Grade 4 titanium cushion design, 3000 nits sapphire display, 10ATM / IP68 water resistance, dual-frequency GPS, Energy Score powered by Galaxy AI, sleep apnea detection, 3nm processor, up to 100 hours power saving mode."
    },
    {
        "product_id": 20,
        "product_name": "Oura Ring Gen 3 Horizon Smart Ring - Stealth Matte Finish with Sleep & HRV Tracking",
        "aisle_id": 103, "department_id": 1, "price": 399.00, "rating": 4.6, "review_count": 3200,
        "brand": "Oura",
        "description": "Sleek titanium smart ring with medical-grade sensors measuring heart rate, heart rate variability (HRV), skin temperature deviations, blood oxygen (SpO2), readiness score, and comprehensive sleep stages with up to 7 days battery."
    },

    # Aisle 104: Smart Home & Security Cameras
    {
        "product_id": 21,
        "product_name": "Google Nest Learning Thermostat 4th Gen with Polished Obsidian Bezel & Dynamic Farsight",
        "aisle_id": 104, "department_id": 1, "price": 279.99, "rating": 4.8, "review_count": 840,
        "brand": "Google Nest",
        "description": "Domed borderless glass display with Dynamic Farsight clock/weather, intelligent energy saving AI schedules, Matter smart home protocol support, bundled Nest Temperature Sensor Gen 2, multi-stage HVAC compatibility."
    },
    {
        "product_id": 22,
        "product_name": "Ring Battery Doorbell Pro with 3D Motion Detection & Bird's Eye View 1536p HD",
        "aisle_id": 104, "department_id": 1, "price": 229.99, "rating": 4.7, "review_count": 1820,
        "brand": "Ring",
        "description": "Head-to-Toe 1536p HD video doorbell with radar-powered 3D Motion Detection, Bird's Eye Zones, color night vision, low-light vision, two-way audio with Audio+ noise cancellation, quick-release rechargeable battery."
    },
    {
        "product_id": 23,
        "product_name": "Philips Hue White and Color Ambiance A19 Smart LED Bulb Starter Kit (4-Pack with Bridge)",
        "aisle_id": 104, "department_id": 1, "price": 199.99, "rating": 4.8, "review_count": 3410,
        "brand": "Philips Hue",
        "description": "16 million vibrant colors and warm-to-cool white light (2000K-6500K), Zigbee & Matter hub included, syncs with movies, gaming (Razer Chroma), and Spotify music, scheduled sunrise wake-up automation, voice assistant compatible."
    },
    {
        "product_id": 24,
        "product_name": "Eufy Security eufyCam S330 (Cam 3) 4K Solar Wireless Outdoor Security Camera 2-Cam Kit",
        "aisle_id": 104, "department_id": 1, "price": 549.99, "rating": 4.7, "review_count": 920,
        "brand": "Eufy",
        "description": "4K Ultra HD cameras with integrated solar panels needing only 2 hours daily sun for infinite power, BionicMind on-device facial recognition AI, HomeBase 3 with expandable local storage up to 16TB, zero monthly subscription fees."
    },

    # Aisle 105: Charging, Power Banks & Cables
    {
        "product_id": 25,
        "product_name": "Anker Prime 27,650mAh Power Bank (250W Multi-Port Fast Output) with Smart Display",
        "aisle_id": 105, "department_id": 1, "price": 179.99, "rating": 4.9, "review_count": 1420,
        "brand": "Anker",
        "description": "Airline-approved 99.54Wh battery pack delivering single-port 140W PD 3.1 or multi-port 250W simultaneous charge, digital color display showing real-time wattages and health, Bluetooth app control, recharges fully in 37 minutes."
    },
    {
        "product_id": 26,
        "product_name": "Anker 3-in-1 MagSafe Foldable Wireless Charger Stand with 15W Qi2 Fast Charging",
        "aisle_id": 105, "department_id": 1, "price": 89.99, "rating": 4.8, "review_count": 2150,
        "brand": "Anker",
        "description": "Compact foldable travel charging station certified for Qi2 15W magnetic fast wireless charging for iPhone, dedicated Apple Watch fast charger, and 5W wireless AirPods pad, includes 40W USB-C wall brick and braided cable."
    },
    {
        "product_id": 27,
        "product_name": "UGREEN Nexode 300W 5-Port GaN Desktop Fast Charger with Dual 140W Laptop Power",
        "aisle_id": 105, "department_id": 1, "price": 199.99, "rating": 4.8, "review_count": 670,
        "brand": "UGREEN",
        "description": "Heavy-duty GaNFast desktop power station with 4 USB-C ports and 1 USB-A port, capable of powering two 16-inch MacBooks at 140W each simultaneously, Thermal Guard 2.0 temperature protection, compact vertical footprint."
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 2. COMPUTERS & GAMING (Dept 2)
    # ══════════════════════════════════════════════════════════════════════════
    # Aisle 201: Laptops & High-Performance Ultrabooks
    {
        "product_id": 28,
        "product_name": "Apple MacBook Pro 16-inch M3 Max (16-core CPU, 40-core GPU, 48GB RAM, 1TB SSD) Space Black",
        "aisle_id": 201, "department_id": 2, "price": 3499.00, "rating": 4.9, "review_count": 920,
        "brand": "Apple",
        "description": "Heavyweight mobile workstation for 3D rendering, 8K video editing, and ML development. 16.2-inch Liquid Retina XDR display with 1600 nits peak HDR brightness and ProMotion 120Hz, M3 Max 3nm chip with hardware ray tracing, 48GB unified memory, 22-hour battery life, 3x Thunderbolt 4, HDMI 2.1, SDXC slot."
    },
    {
        "product_id": 29,
        "product_name": "Apple MacBook Air 13-inch M3 (8-core CPU, 10-core GPU, 16GB RAM, 512GB SSD) Midnight",
        "aisle_id": 201, "department_id": 2, "price": 1299.00, "rating": 4.9, "review_count": 2400,
        "brand": "Apple",
        "description": "Ultraportable fanless aluminum laptop weighing 2.7 lbs, M3 chip with support for dual external displays with laptop lid closed, 13.6-inch Liquid Retina display with 500 nits, MagSafe 3 charging, 18 hours battery life, 1080p FaceTime HD camera."
    },
    {
        "product_id": 30,
        "product_name": "Dell XPS 16 9640 Laptop OLED 4K (Intel Core Ultra 9 185H, 32GB RAM, 1TB SSD, RTX 4070)",
        "aisle_id": 201, "department_id": 2, "price": 2799.99, "rating": 4.6, "review_count": 480,
        "brand": "Dell",
        "description": "Machined aluminum and CNC glass chassis, 16.3-inch 4K+ (3840x2400) InfinityEdge OLED touchscreen with 100% DCI-P3 color accuracy, Intel Core Ultra 9 processor with dedicated NPU for AI, NVIDIA GeForce RTX 4070 8GB GDDR6, capacitive touch function row, invisible glass haptic touchpad."
    },
    {
        "product_id": 31,
        "product_name": "Lenovo ThinkPad X1 Carbon Gen 12 (Intel Core Ultra 7 155H, 32GB RAM, 1TB SSD) Ultralight",
        "aisle_id": 201, "department_id": 2, "price": 1949.00, "rating": 4.8, "review_count": 610,
        "brand": "Lenovo",
        "description": "Iconic enterprise business laptop weighing just 2.42 lbs with carbon fiber top cover, legendary tactile ThinkPad keyboard with TrackPoint, 14-inch 2.8K OLED 120Hz anti-glare display, MIL-STD-810H durability certified, dual Thunderbolt 4 ports, Wi-Fi 7."
    },
    {
        "product_id": 32,
        "product_name": "ASUS ROG Zephyrus G16 Gaming Laptop OLED (Intel Core Ultra 9, RTX 4080, 32GB RAM, 2TB SSD)",
        "aisle_id": 201, "department_id": 2, "price": 2699.99, "rating": 4.8, "review_count": 590,
        "brand": "ASUS",
        "description": "Ultra-slim 1.95kg CNC aluminum gaming laptop, 16-inch 2.5K 240Hz 0.2ms ROG Nebula OLED display with G-SYNC, NVIDIA GeForce RTX 4080 12GB laptop GPU, Slash Lighting customizable lid LED array, vapor chamber cooling, 90Wh fast-charge battery."
    },
    {
        "product_id": 33,
        "product_name": "Razer Blade 14 Compact Gaming Laptop (AMD Ryzen 9 8945HS, RTX 4070, 32GB DDR5, 1TB SSD)",
        "aisle_id": 201, "department_id": 2, "price": 2399.99, "rating": 4.7, "review_count": 410,
        "brand": "Razer",
        "description": "Anodized CNC matte black aluminum unibody, 14-inch QHD+ 240Hz 16:10 display, AMD Ryzen 9 processor with Ryzen AI NPU, RTX 4070 GPU, expandable dual-channel DDR5 memory, per-key RGB Chroma lighting, vapor chamber cooling."
    },

    # Aisle 202: Monitors & High-Refresh Displays
    {
        "product_id": 34,
        "product_name": "LG UltraGear 34GS95QE 34-inch Curved OLED 240Hz 0.03ms WQHD Gaming Monitor 800R",
        "aisle_id": 202, "department_id": 2, "price": 999.99, "rating": 4.8, "review_count": 620,
        "brand": "LG",
        "description": "Immersive 800R curved 34-inch WQHD (3440 x 1440) Ultra-Gear OLED panel, blisteringly fast 240Hz refresh rate and 0.03ms (GtG) response time, VESA DisplayHDR True Black 400, 98.5% DCI-P3 color gamut, NVIDIA G-SYNC Compatible and AMD FreeSync Premium Pro, HDMI 2.1 & DisplayPort 1.4."
    },
    {
        "product_id": 35,
        "product_name": "Dell UltraSharp 32-inch 4K Thunderbolt 4 Hub Monitor (U3224KB) 6K IPS Black",
        "aisle_id": 202, "department_id": 2, "price": 1499.99, "rating": 4.7, "review_count": 310,
        "brand": "Dell",
        "description": "Professional creator monitor with 6K (6144 x 3456) resolution and IPS Black technology providing 2000:1 contrast ratio, built-in 4K HDR Sony STARVIS dual-gain webcam, echo-canceling dual mics, 140W Thunderbolt 4 pass-through charging, 99% DCI-P3."
    },
    {
        "product_id": 36,
        "product_name": "ASUS ProArt Display 27-inch 4K HDR Color-Accurate Professional Monitor (PA279CRV)",
        "aisle_id": 202, "department_id": 2, "price": 499.00, "rating": 4.8, "review_count": 1120,
        "brand": "ASUS",
        "description": "Calman Verified factory pre-calibrated 4K UHD (3840 x 2160) IPS display with Delta E < 2 color accuracy, 99% DCI-P3 and 99% Adobe RGB coverage, 96W USB-C single cable power and video delivery, ergonomic swivel, tilt, pivot, and height-adjustable stand."
    },

    # Aisle 203: Gaming Consoles & Handhelds
    {
        "product_id": 37,
        "product_name": "Sony PlayStation 5 Pro Console 2TB SSD with Spectral Super Resolution (PSSR) 4K Ray Tracing",
        "aisle_id": 203, "department_id": 2, "price": 699.99, "rating": 4.7, "review_count": 870,
        "brand": "Sony PlayStation",
        "description": "Upgraded PS5 Pro GPU with 67% more Compute Units, advanced ray tracing performance up to 3x faster, AI-driven PlayStation Spectral Super Resolution (PSSR) upscaling for smooth 60fps and 120fps 4K gaming, 2TB high-speed NVMe internal storage, Wi-Fi 7."
    },
    {
        "product_id": 38,
        "product_name": "Nintendo Switch OLED Model - White Joy-Con with 7-inch Vibrant Screen & 64GB",
        "aisle_id": 203, "department_id": 2, "price": 349.99, "rating": 4.9, "review_count": 9400,
        "brand": "Nintendo",
        "description": "Hybrid home console and handheld gaming system featuring 7-inch OLED multi-touch display with vivid colors and deep blacks, wide adjustable tabletop kickstand, dock with wired LAN ethernet port, enhanced onboard audio, 64GB internal storage."
    },
    {
        "product_id": 39,
        "product_name": "Steam Deck OLED 1TB Handheld PC Gaming Console with 90Hz HDR Screen & Anti-Glare Glass",
        "aisle_id": 203, "department_id": 2, "price": 649.00, "rating": 4.9, "review_count": 3100,
        "brand": "Valve",
        "description": "Portable PC gaming powerhouse with 7.4-inch 90Hz HDR OLED display delivering 1000 nits peak brightness, etched anti-glare glass, 50Wh battery for 3-12 hours of gameplay, Wi-Fi 6E, redesigned thumbsticks with trackpads and gyro controls, SteamOS library access."
    },

    # Aisle 204: Mechanical Keyboards & Gaming Mice
    {
        "product_id": 40,
        "product_name": "Keychron Q1 Pro Wireless Custom Mechanical Keyboard 75% CNC Aluminum with Gateron Jupiter",
        "aisle_id": 204, "department_id": 2, "price": 199.99, "rating": 4.8, "review_count": 920,
        "brand": "Keychron",
        "description": "Full CNC machined 6063 aluminum body, double-gasket acoustic mounting design, hot-swappable switch sockets, Bluetooth 5.1 & Type-C wired connection, QMK/VIA programmable layout, South-facing RGB backlighting, compatible with macOS and Windows."
    },
    {
        "product_id": 41,
        "product_name": "Logitech MX Master 3S Wireless Performance Mouse with 8K DPI Sensor & Quiet Clicks",
        "aisle_id": 204, "department_id": 2, "price": 99.99, "rating": 4.9, "review_count": 5200,
        "brand": "Logitech",
        "description": "Ergonomic master mouse with MagSpeed electromagnetic scroll wheel scrolling 1000 lines per second, 8000 DPI Darkfield tracking on glass, 90% quieter clicks, thumb gesture button and horizontal thumb wheel, multi-device Logitech Flow cross-computer control."
    },
    {
        "product_id": 42,
        "product_name": "Logitech G PRO X SUPERLIGHT 2 Wireless Ultra-Lightweight Gaming Mouse 60g 32K DPI",
        "aisle_id": 204, "department_id": 2, "price": 159.99, "rating": 4.8, "review_count": 1410,
        "brand": "Logitech G",
        "description": "Pro esports wireless mouse weighing only 60 grams, LIGHTFORCE hybrid optical-mechanical switches, HERO 2 sensor with 32000 DPI and over 500 IPS tracking, 2000Hz polling rate, zero-additive PTFE glide feet, 95 hours continuous battery life."
    },

    # Aisle 205: Fast External Storage & Docks
    {
        "product_id": 43,
        "product_name": "Samsung T9 Portable SSD 2TB Rugged External NVMe Drive USB 3.2 Gen 2x2 (2000MB/s)",
        "aisle_id": 205, "department_id": 2, "price": 219.99, "rating": 4.8, "review_count": 1820,
        "brand": "Samsung",
        "description": "Pocket-sized rugged SSD with up to 2000MB/s sequential read/write speeds over USB 3.2 Gen 2x2, rubberized non-slip exterior protecting against drops up to 3 meters, Dynamic Thermal Guard prevents overheating during massive video transfers."
    },
    {
        "product_id": 44,
        "product_name": "CalDigit TS4 Thunderbolt 4 18-Port Dock Station with 98W Charging & Dual 4K 60Hz",
        "aisle_id": 205, "department_id": 2, "price": 399.95, "rating": 4.8, "review_count": 980,
        "brand": "CalDigit",
        "description": "Ultimate desktop dock with 18 ports including 3x Thunderbolt 4, 5x USB-A, 3x USB-C (up to 20W), 2.5 Gigabit Ethernet, DisplayPort 1.4, SD/microSD UHS-II readers, dual audio jacks, and 98W host laptop fast charging."
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 3. AUDIO & SOUND (Dept 3)
    # ══════════════════════════════════════════════════════════════════════════
    # Aisle 301: Active Noise Cancelling Over-Ear Headphones
    {
        "product_id": 45,
        "product_name": "Sony WH-1000XM5 Wireless Industry-Leading Noise Cancelling Headphones with Auto NC Optimizer",
        "aisle_id": 301, "department_id": 3, "price": 398.00, "rating": 4.8, "review_count": 4200,
        "brand": "Sony",
        "description": "Two processors and 8 microphones for world-class active noise cancellation, custom 30mm carbon fiber composite driver, LDAC high-res audio codec, 4 beamforming microphones with AI noise reduction for crystal calls, 30 hours battery life with 3 min quick charge for 3 hours."
    },
    {
        "product_id": 46,
        "product_name": "Bose QuietComfort Ultra Headphones with Spatial Audio & CustomTune Sound Calibration",
        "aisle_id": 301, "department_id": 3, "price": 429.00, "rating": 4.7, "review_count": 2150,
        "brand": "Bose",
        "description": "Breakthrough Bose Immersive Audio spatial sound, world-class active noise cancelling with CustomTune technology tailoring sound to individual ear shape, plush protein leather earcups, 24 hours battery life, multipoint Bluetooth 5.3 connection."
    },
    {
        "product_id": 47,
        "product_name": "Apple AirPods Max (USB-C) Over-Ear Headphones with Personalized Spatial Audio - Midnight",
        "aisle_id": 301, "department_id": 3, "price": 549.00, "rating": 4.7, "review_count": 2890,
        "brand": "Apple",
        "description": "Knit mesh canopy headband with anodized aluminum earcups, Apple-designed 40mm dynamic driver, dual H1 chips for computational audio, pro-level Active Noise Cancellation with Transparency mode, USB-C lossless audio input and charging, 20 hours battery life."
    },
    {
        "product_id": 48,
        "product_name": "Sennheiser Momentum 4 Wireless Audiophile Headphones with 60-Hour Battery Life",
        "aisle_id": 301, "department_id": 3, "price": 299.95, "rating": 4.6, "review_count": 1640,
        "brand": "Sennheiser",
        "description": "Signature Sennheiser sound driven by 42mm audiophile-inspired transducer system, adaptive active noise cancellation with adjustable transparency mode, industry-dominating 60-hour battery life on a single charge, aptX Adaptive codec support."
    },

    # Aisle 302: True Wireless Noise-Cancelling Earbuds
    {
        "product_id": 49,
        "product_name": "Apple AirPods Pro 2 Wireless Earbuds with USB-C MagSafe Case & Active Noise Cancellation",
        "aisle_id": 302, "department_id": 3, "price": 249.00, "rating": 4.9, "review_count": 6800,
        "brand": "Apple",
        "description": "H2 chip providing up to 2x more Active Noise Cancellation, Adaptive Audio dynamically blending ANC and Transparency based on noise environment, Conversation Awareness, personalized spatial audio with dynamic head tracking, IP54 dust/sweat/water resistance, hearing aid clinical feature."
    },
    {
        "product_id": 50,
        "product_name": "Sony WF-1000XM5 True Wireless Noise Cancelling Earbuds with Dynamic Driver X",
        "aisle_id": 302, "department_id": 3, "price": 299.99, "rating": 4.6, "review_count": 2100,
        "brand": "Sony",
        "description": "Integrated Processor V2 and QN2e HD noise cancelling processor, Dynamic Driver X for wide frequency reproduction and rich vocals, bone conduction sensors for wind-noise-free clear calls, polyurethane foam ear tips, LDAC support, IPX4 water resistance."
    },
    {
        "product_id": 51,
        "product_name": "Bose QuietComfort Ultra Wireless Earbuds with Immersive Spatial Audio",
        "aisle_id": 302, "department_id": 3, "price": 299.00, "rating": 4.6, "review_count": 1720,
        "brand": "Bose",
        "description": "Unrivaled in-ear active noise cancellation with CustomTune audio calibration to ear canal acoustics, revolutionary spatial audio, umbrella-shaped soft silicone ear tips with stability bands, touch controls, IPX4 sweat and weather resistance."
    },

    # Aisle 303: Waterproof Bluetooth Speakers
    {
        "product_id": 52,
        "product_name": "JBL Charge 5 Portable Waterproof Bluetooth Speaker with Built-in Powerbank (IP67)",
        "aisle_id": 303, "department_id": 3, "price": 179.95, "rating": 4.8, "review_count": 5100,
        "brand": "JBL",
        "description": "Optimized long excursion driver, separate tweeter, and dual pumping JBL bass radiators, IP67 waterproof and dustproof for pool, beach, and rain, up to 20 hours playtime, integrated USB powerbank to charge smartphones on the go, PartyBoost pairing."
    },
    {
        "product_id": 53,
        "product_name": "Sonos Roam 2 Ultra-Portable Smart Waterproof Bluetooth and Wi-Fi Speaker",
        "aisle_id": 303, "department_id": 3, "price": 179.00, "rating": 4.7, "review_count": 1280,
        "brand": "Sonos",
        "description": "Compact speaker seamlessly switching between Bluetooth outdoor audio and home Wi-Fi multiroom network, Automatic Trueplay tuning adapting sound to surroundings, IP67 waterproof (submersible up to 3 feet for 30 minutes), 10 hours battery life."
    },
    {
        "product_id": 54,
        "product_name": "Ultimate Ears MEGABOOM 3 360-Degree Deep Bass Wireless Speaker (Waterproof & Floats)",
        "aisle_id": 303, "department_id": 3, "price": 199.99, "rating": 4.7, "review_count": 3400,
        "brand": "Ultimate Ears",
        "description": "Immersive 360-degree room-filling sound with thundering deep bass, IP67 water and dustproof that actually floats in pool water, Magic Button to play/pause/skip tracks, rugged two-tone performance fabric, 20 hours battery life."
    },

    # Aisle 304: Home Theater Soundbars & Audio Systems
    {
        "product_id": 55,
        "product_name": "Sonos Arc Premium Smart Soundbar with Dolby Atmos & Speech Enhancement",
        "aisle_id": 304, "department_id": 3, "price": 899.00, "rating": 4.8, "review_count": 2980,
        "brand": "Sonos",
        "description": "Eleven high-performance drivers including upward-firing elliptical woofers delivering immersive 3D Dolby Atmos soundstage, tuned by Oscar-winning sound engineers, Speech Enhancement for crystal-clear TV dialogue, HDMI eARC, Apple AirPlay 2."
    },
    {
        "product_id": 56,
        "product_name": "Bose Smart Ultra Soundbar with Dolby Atmos & A.I. Dialogue Mode",
        "aisle_id": 304, "department_id": 3, "price": 899.00, "rating": 4.7, "review_count": 1420,
        "brand": "Bose",
        "description": "Nine speakers including two upward-firing dipole transducers, TrueSpace spatial processing upmixing non-Atmos content, AI Dialogue Mode automatically balancing vocal clarity over background action explosions, HDMI eARC, Wi-Fi and Bluetooth."
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 4. HOME & KITCHEN APPLIANCES (Dept 4)
    # ══════════════════════════════════════════════════════════════════════════
    # Aisle 401: Espresso Machines & Coffee Grinders
    {
        "product_id": 57,
        "product_name": "Breville Barista Touch Impress Espresso Machine with Auto MilQ and Assisted Tamping",
        "aisle_id": 401, "department_id": 4, "price": 1499.95, "rating": 4.9, "review_count": 860,
        "brand": "Breville",
        "description": "All-in-one home barista station featuring intuitive touchscreen walkthrough, Impress Puck System with 7-degree barista twist and 22 lbs assisted tamping, Auto MilQ hands-free microfoam texturing with settings for oat, almond, and dairy milk, ThermoJet 3-second rapid heat-up."
    },
    {
        "product_id": 58,
        "product_name": "Fellow Ode Gen 2 Electric Brew Coffee Grinder with 64mm Flat Burrs & Antistatic",
        "aisle_id": 401, "department_id": 4, "price": 345.00, "rating": 4.8, "review_count": 1250,
        "brand": "Fellow",
        "description": "Precision cafe-grade single-dose home grinder engineered specifically for pour-over, drip, and French press. 64mm professional stainless steel flat burrs, 31 stepped grind settings, ion technology drastically reducing static mess, quiet auto-stop motor."
    },
    {
        "product_id": 59,
        "product_name": "De'Longhi Magnifica S Fully Automatic Bean-to-Cup Espresso and Cappuccino Machine",
        "aisle_id": 401, "department_id": 4, "price": 649.95, "rating": 4.7, "review_count": 3100,
        "brand": "De'Longhi",
        "description": "Compact bean-to-cup machine grinding fresh coffee beans at the touch of a button with 13 adjustable settings, 15-bar pressure pump, manual traditional milk frother steam wand for creamy cappuccinos, removable brew unit for effortless cleaning."
    },

    # Aisle 402: Air Fryers, Blenders & Kitchen Tech
    {
        "product_id": 60,
        "product_name": "Ninja Speedi Rapid Cooker & Air Fryer 6-Quart 12-in-1 (Meals in 15 Minutes)",
        "aisle_id": 402, "department_id": 4, "price": 199.99, "rating": 4.8, "review_count": 2780,
        "brand": "Ninja",
        "description": "Speedi Rapid Cooker system simultaneously steams base grains/pastas and air-crisps proteins in one 6-quart pot in under 15 minutes, 12 versatile functions including steam & crisp, proof, bake, dehydrate, and sear/saute, non-stick ceramic pot."
    },
    {
        "product_id": 61,
        "product_name": "Vitamix A3500 Ascent Series Smart Professional-Grade Blender with Touchscreen & Timers",
        "aisle_id": 402, "department_id": 4, "price": 699.95, "rating": 4.9, "review_count": 2940,
        "brand": "Vitamix",
        "description": "Commercial-grade 2.2 peak HP motor, laser-cut hardened stainless steel aircraft blades, 5 program presets (smoothies, hot soups, dips, frozen desserts, self-cleaning), programmable countdown digital timer, Self-Detect container technology, 10-year warranty."
    },
    {
        "product_id": 62,
        "product_name": "Cosori TurboBlaze 6.0-Quart Air Fryer with DC Motor Tech & 9 Cooking Functions",
        "aisle_id": 402, "department_id": 4, "price": 119.99, "rating": 4.7, "review_count": 1890,
        "brand": "Cosori",
        "description": "Energy-efficient brushless DC motor with 5 fan speed controls cooking food up to 46% faster, wide temperature range from 90°F (dehydrating/fermenting) up to 450°F (crisp broiling), nonstick dishwasher-safe basket."
    },

    # Aisle 403: Cast Iron, Knives & Premium Cookware
    {
        "product_id": 63,
        "product_name": "Le Creuset Enameled Cast Iron Signature Round Dutch Oven 5.5 Qt - Cerise Red",
        "aisle_id": 403, "department_id": 4, "price": 419.95, "rating": 4.9, "review_count": 3800,
        "brand": "Le Creuset",
        "description": "Handcrafted in France since 1925, superior heat distribution and retention, durable sand-colored interior enamel resisting chipping and dulling, tight-fitting lid with heat-resistant composite knob safe up to 500°F, induction and oven compatible."
    },
    {
        "product_id": 64,
        "product_name": "Shun Classic 8-inch Chef's Knife Japanese VG-MAX Damascus Steel (Handcrafted in Japan)",
        "aisle_id": 403, "department_id": 4, "price": 169.95, "rating": 4.9, "review_count": 2450,
        "brand": "Shun",
        "description": "Proprietary VG-MAX cutting core clad with 34 micro-layers of Damascus stainless steel on each side, razor-sharp 16-degree double-bevel cutting edge, moisture-resistant D-shaped Pakkawood handle providing comfortable grip and balance."
    },

    # Aisle 404: Robot Vacuums & Cordless Cleaning
    {
        "product_id": 65,
        "product_name": "Roborock S8 Pro Ultra Robot Vacuum and Mop with RockDock All-in-One Auto Clean Station",
        "aisle_id": 404, "department_id": 4, "price": 1399.99, "rating": 4.8, "review_count": 1100,
        "brand": "Roborock",
        "description": "RockDock Ultra automatically washes mop, hot-air dries, empties dustbin for up to 7 weeks, and refills water tank. 6000Pa intense suction, DuoRoller Riser dual rubber brushes resisting hair tangles, VibraRise 2.0 sonic mopping scrubbing at 3000 times/min, Reactive 3D obstacle avoidance."
    },
    {
        "product_id": 66,
        "product_name": "Dyson V15 Detect Cordless Vacuum Cleaner with Fluffy Optic Laser & Piezo Dust Sensor",
        "aisle_id": 404, "department_id": 4, "price": 749.99, "rating": 4.8, "review_count": 2890,
        "brand": "Dyson",
        "description": "Fluffy Optic cleaner head illuminates microscopic dust on hard floors, acoustic piezo sensor counts and measures dust particles automatically increasing suction power when needed, LCD screen shows proof of deep clean, up to 60 minutes runtime."
    },

    # Aisle 405: Air Purifiers & Smart Climate Control
    {
        "product_id": 67,
        "product_name": "Dyson Purifier Hot+Cool Formaldehyde HP09 Smart Air Purifier Heater & Fan",
        "aisle_id": 405, "department_id": 4, "price": 799.99, "rating": 4.7, "review_count": 1420,
        "brand": "Dyson",
        "description": "Solid-state formaldehyde sensor permanently destroys formaldehyde molecules, fully sealed HEPA H13 filtration capturing 99.97% of particles down to 0.3 microns, Air Multiplier technology projecting purified heat or cool air across the whole room, 350-degree oscillation."
    },
    {
        "product_id": 68,
        "product_name": "Levoit Core 400S Smart True HEPA Air Purifier for Large Rooms with Real-Time PM2.5",
        "aisle_id": 405, "department_id": 4, "price": 219.99, "rating": 4.8, "review_count": 4600,
        "brand": "Levoit",
        "description": "VortexAir Technology cleans rooms up to 1,980 sq ft in one hour, H13 True HEPA 3-stage filtration with activated carbon filter trapping pet odors, smoke, and pollen, AirSight Plus laser dust sensor detects real-time air quality on color display, works with Alexa."
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 5. FASHION & OUTERWEAR (Dept 5)
    # ══════════════════════════════════════════════════════════════════════════
    # Aisle 501: Weatherproof Jackets & Down Parkas
    {
        "product_id": 69,
        "product_name": "Arc'teryx Beta AR Waterproof GORE-TEX PRO Jacket (All-Round Alpine Shell)",
        "aisle_id": 501, "department_id": 5, "price": 600.00, "rating": 4.9, "review_count": 780,
        "brand": "Arc'teryx",
        "description": "Rugged alpine shell constructed with most breathable GORE-TEX PRO Most Rugged technology, DropHood helmet-compatible storm hood with internal collar, WaterTight pit zips for ventilation, articulated patterning for athletic movement, RECCO avalanche reflector."
    },
    {
        "product_id": 70,
        "product_name": "Patagonia Down Sweater Hoody Lightweight 800-Fill-Power Recycled Goose Down",
        "aisle_id": 501, "department_id": 5, "price": 329.00, "rating": 4.9, "review_count": 2100,
        "brand": "Patagonia",
        "description": "Windproof shell made of 100% postconsumer recycled nylon ripstop from recycled fishing nets (NetPlus), insulated with 800-fill-power 100% Responsible Down Standard goose down, single-pull adjustable hood, internal zippered chest pocket doubles as stuffsack."
    },
    {
        "product_id": 71,
        "product_name": "The North Face 1996 Retro Nuptse Jacket 700-Fill Goose Down Water-Repellent Puffer",
        "aisle_id": 501, "department_id": 5, "price": 330.00, "rating": 4.8, "review_count": 3200,
        "brand": "The North Face",
        "description": "Iconic boxy silhouette with oversized baffles inspired by 1996 design, durable ripstop fabric with non-PFC DWR water-repellent finish, certified 700-fill goose down insulation providing lightweight warmth, stowable hood packs into collar."
    },

    # Aisle 502: Premium Hoodies, Sweaters & Flannels
    {
        "product_id": 72,
        "product_name": "Reigning Champ Heavyweight Fleece Pullover Hoodie (Handcrafted in Canada)",
        "aisle_id": 502, "department_id": 5, "price": 175.00, "rating": 4.8, "review_count": 680,
        "brand": "Reigning Champ",
        "description": "Handcrafted in Vancouver from signature 100% cotton Heavyweight Fleece, flatlock seam construction, semi-raglan sleeves, dual-layer hood with knotted cotton drawcords, ribbed side gussets providing comfort and shape retention."
    },
    {
        "product_id": 73,
        "product_name": "Filson Alaskan Guide Heavyweight Brushed Cotton Flannel Shirt - Red/Black Plaid",
        "aisle_id": 502, "department_id": 5, "price": 145.00, "rating": 4.9, "review_count": 1400,
        "brand": "Filson",
        "description": "Dense 8-oz. 100% cotton flannel brushed on both sides for soft insulation and wind resistance, pleated rear shoulders for full swinging arm mobility, dual button-flap chest pockets, built for decades of cold-weather ranch and outdoor work."
    },

    # Aisle 503: Denim Jeans & Everyday Chinos
    {
        "product_id": 74,
        "product_name": "Levi's 501 Original Fit Jeans 100% Cotton Raw Selvedge Denim with Button Fly",
        "aisle_id": 503, "department_id": 5, "price": 98.00, "rating": 4.7, "review_count": 6400,
        "brand": "Levi's",
        "description": "The quintessential blue jean since 1873. Classic straight leg with authentic button fly, sits at the natural waist, crafted from sturdy 100% non-stretch cotton denim that forms uniquely to the wearer's body over time."
    },
    {
        "product_id": 75,
        "product_name": "Lululemon ABC Classic-Fit Trouser 32L Warpstreme Wrinkle-Resistant Pant",
        "aisle_id": 503, "department_id": 5, "price": 128.00, "rating": 4.8, "review_count": 3100,
        "brand": "Lululemon",
        "description": "Ergonomic ABC (Anti-Ball Crushing) gusset design delivering all-day commuter freedom, four-way stretch Warpstreme fabric that resists wrinkles and sheds light moisture, hidden zippered back passport pocket, refined modern trouser styling."
    },

    # Aisle 504: Performance Activewear & Gym Apparel
    {
        "product_id": 76,
        "product_name": "Lululemon Pace Breaker Linerless Short 7-inch Lightweight Stretch Gym Workout",
        "aisle_id": 504, "department_id": 5, "price": 68.00, "rating": 4.9, "review_count": 4200,
        "brand": "Lululemon",
        "description": "Ultra-lightweight four-way stretch Swift fabric with sweat-wicking and quick-drying properties, low-bounce zippered side pocket keeps phone securely anchored during sprints, flat waistband with reversible drawstring."
    },
    {
        "product_id": 77,
        "product_name": "Gymshark Apex Seamless T-Shirt Breathable Jacquard Knit High-Ventilation Training",
        "aisle_id": 504, "department_id": 5, "price": 54.00, "rating": 4.6, "review_count": 920,
        "brand": "Gymshark",
        "description": "Heat-mapping ventilation zones woven into lightweight seamless construction, anti-chafing ergonomic flat seams, sweat-wicking E-DRY treatment, slim athletic fit accentuating shoulders and chest during heavy weightlifting sessions."
    },

    # Aisle 505: Travel Bags, Wallets & Backpacks
    {
        "product_id": 78,
        "product_name": "Bellroy Classic Backpack Plus 24L Weatherproof Laptop Travel Daypack - Black",
        "aisle_id": 505, "department_id": 5, "price": 179.00, "rating": 4.8, "review_count": 1450,
        "brand": "Bellroy",
        "description": "Water-resistant recycled Baida woven fabric with environmentally certified leather details, separate padded compartment fits up to 16-inch laptops with Aquaguard zipper, dual slide water bottle pockets, lumbar support back panel, hidden sunglasses valet."
    },
    {
        "product_id": 79,
        "product_name": "Peak Design Everyday Backpack 30L V2 Camera & Tech Travel Pack with MagLatch",
        "aisle_id": 505, "department_id": 5, "price": 299.95, "rating": 4.8, "review_count": 2150,
        "brand": "Peak Design",
        "description": "Versatile camera and tech backpack with customizable origami-inspired FlexFold dividers, weatherproof 100% recycled 400D double poly-coated canvas shell, fast dual side access zippers, magnetic MagLatch hardware expanding storage by 8L."
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 6. FOOTWEAR & ATHLETIC SHOES (Dept 6)
    # ══════════════════════════════════════════════════════════════════════════
    # Aisle 601: Road & Trail Running Shoes
    {
        "product_id": 80,
        "product_name": "Nike Alphafly 3 Road Marathon Racing Shoes with Dual Air Zoom Units & Carbon Flyplate",
        "aisle_id": 601, "department_id": 6, "price": 285.00, "rating": 4.9, "review_count": 890,
        "brand": "Nike",
        "description": "Marathon world record racing shoe engineered with continuous ZoomX foam midsole, full-length curved carbon fiber Flyplate for maximum propulsion, dual forefoot Air Zoom pods, Atomknit 3.0 breathable upper providing lockdown without weight."
    },
    {
        "product_id": 81,
        "product_name": "Hoka Bondi 8 Maximum Cushion Running Shoes for High Mileage & Recovery Running",
        "aisle_id": 601, "department_id": 6, "price": 165.00, "rating": 4.8, "review_count": 5200,
        "brand": "Hoka",
        "description": "One of the most plushly cushioned running shoes in the world. Ultra-lightweight resilient foam midsole, extended heel with billowed grooves for smooth heel-to-toe transition, engineered mesh upper, ortholite hybrid sockliner, APMA accepted for foot health."
    },
    {
        "product_id": 82,
        "product_name": "Brooks Ghost 16 Daily Neutral Cushion Running Shoes with Nitrogen-Infused DNA LOFT v3",
        "aisle_id": 601, "department_id": 6, "price": 140.00, "rating": 4.8, "review_count": 4800,
        "brand": "Brooks",
        "description": "Reliable daily workhorse featuring nitrogen-infused DNA LOFT v3 cushioning delivering lightweight plush bounce, Segmented Crash Pad shock absorber, breathable engineered air mesh upper, certified carbon neutral."
    },
    {
        "product_id": 83,
        "product_name": "Salomon Speedcross 6 GORE-TEX Waterproof Aggressive Mud Trail Running Shoes",
        "aisle_id": 601, "department_id": 6, "price": 160.00, "rating": 4.8, "review_count": 2100,
        "brand": "Salomon",
        "description": "Legendary off-road grip with deep chevron Mud Contagrip lugs shedding mud rapidly, waterproof breathable GORE-TEX membrane, SensiFit upper cradling the foot, Quicklace one-pull minimalist lacing system with lace pocket."
    },

    # Aisle 602: Lifestyle Sneakers & Classics
    {
        "product_id": 84,
        "product_name": "New Balance 990v6 Made in USA Suede & Mesh Heritage Running Sneaker - Grey",
        "aisle_id": 602, "department_id": 6, "price": 199.99, "rating": 4.8, "review_count": 1850,
        "brand": "New Balance",
        "description": "Handcrafted in the USA with premium pigskin suede and breathable mesh uppers, FuelCell foam delivers propulsive cushioning, ENCAP midsole technology with lightweight polyurethane rim provides all-day structural stability and arch support."
    },
    {
        "product_id": 85,
        "product_name": "Adidas Samba Classic Leather Indoor Soccer & Street Sneaker - Core Black/White",
        "aisle_id": 602, "department_id": 6, "price": 90.00, "rating": 4.7, "review_count": 8900,
        "brand": "Adidas",
        "description": "Timeless icon with soft full-grain leather upper, contrasting suede T-toe overlay, lightweight die-cut EVA insole, low-profile non-marking gum rubber outsole delivering retro street style and skate-ready traction."
    },

    # Aisle 603: Waterproof Hiking Boots & Outdoor Shoes
    {
        "product_id": 86,
        "product_name": "Merrell Moab 3 Mid GORE-TEX Waterproof Hiking Boots (The Mother of All Boots)",
        "aisle_id": 603, "department_id": 6, "price": 155.00, "rating": 4.8, "review_count": 6400,
        "brand": "Merrell",
        "description": "America's favorite hiker with waterproof GORE-TEX membrane, pigskin leather and breathable mesh upper, Vibram TC5+ sticky rubber lug outsole, Kinetic Fit ADVANCED contoured footbed with reinforced heel cushioning for all-day trail comfort."
    },
    {
        "product_id": 87,
        "product_name": "Salomon Quest 4 GORE-TEX Heavy Backpacking Support Mountain Hiking Boots",
        "aisle_id": 603, "department_id": 6, "price": 230.00, "rating": 4.8, "review_count": 1280,
        "brand": "Salomon",
        "description": "High-cut expedition boot featuring 4D Advanced Chassis protecting sensitive joint articulations while carrying heavy 50+ lb backpacks on rocky uneven mountain terrain, full nubuck leather upper with GORE-TEX weatherproofing."
    },

    # Aisle 604: Recovery Slides & Comfort Footwear
    {
        "product_id": 88,
        "product_name": "OOFOS OOriginal Post-Run Recovery Slide Sandal with Impact-Absorbing OOfoam",
        "aisle_id": 604, "department_id": 6, "price": 59.95, "rating": 4.8, "review_count": 7200,
        "brand": "OOFOS",
        "description": "Revolutionary patented OOfoam technology absorbs 37% more impact than traditional EVA footwear foam, biomechanically designed footbed cradles arches to reduce stress on sore knees, ankles, and plantar fasciitis feet."
    },
    {
        "product_id": 89,
        "product_name": "Birkenstock Arizona Essentials EVA Waterproof Lightweight Two-Strap Slide",
        "aisle_id": 604, "department_id": 6, "price": 49.95, "rating": 4.7, "review_count": 6100,
        "brand": "Birkenstock",
        "description": "Molded from ultra-lightweight, flexible, and shock-absorbing EVA foam, anatomically shaped footbed with deep heel cup and arch support, 100% waterproof and washable—ideal for the beach, garden, gym locker room, or poolside."
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 7. SPORTS, FITNESS & OUTDOORS (Dept 7)
    # ══════════════════════════════════════════════════════════════════════════
    # Aisle 701: Smart Fitness Trackers & Gym Tech
    {
        "product_id": 90,
        "product_name": "Theragun PRO Plus 6-in-1 Percussive Therapy Device with Near-Infrared LED & Heat",
        "aisle_id": 701, "department_id": 7, "price": 599.00, "rating": 4.9, "review_count": 740,
        "brand": "Therabody",
        "description": "Medical device cleared 6-in-1 percussive massage gun with 16mm amplitude reaching 60% deeper into muscle tissue, near-infrared LED light therapy for deep tissue circulation, rapid heating attachment, vibration therapy, breathwork biometric heart rate sensor."
    },
    {
        "product_id": 91,
        "product_name": "WHOOP 4.0 Wireless Fitness & Sleep Tracker Band with 12-Month Membership Included",
        "aisle_id": 701, "department_id": 7, "price": 239.00, "rating": 4.5, "review_count": 3100,
        "brand": "WHOOP",
        "description": "Screenless 24/7 biometric health tracker measuring sleep architecture, physiological strain, recovery score, skin temperature, and blood oxygen levels, wireless waterproof battery pack charges while wearing, any-wear sensor compatibility."
    },

    # Aisle 702: Adjustable Dumbbells, Mats & Recovery
    {
        "product_id": 92,
        "product_name": "Bowflex SelectTech 552 Adjustable Dumbbells Pair (Rapid Dial 5 to 52.5 lbs)",
        "aisle_id": 702, "department_id": 7, "price": 429.00, "rating": 4.8, "review_count": 8900,
        "brand": "Bowflex",
        "description": "Space-saving mechanical dial system replaces 15 sets of weights in one compact footprint, adjusts in 2.5 lb increments up to 25 lbs and 5 lb increments up to 52.5 lbs, durable molding over metal plates provides smooth quiet lifts."
    },
    {
        "product_id": 93,
        "product_name": "Manduka PRO Yoga Mat 6mm Extra Thick High-Density Cushion Non-Slip Lifetime Guarantee",
        "aisle_id": 702, "department_id": 7, "price": 138.00, "rating": 4.9, "review_count": 4100,
        "brand": "Manduka",
        "description": "Legendary ultra-dense 6mm cushion protects joints on hard floors, closed-cell surface prevents sweat and bacteria from absorbing into the mat, proprietary dot pattern bottom grips floors firmly, OEKO-TEX certified non-toxic manufacturing."
    },

    # Aisle 703: Camping Tents, Sleeping Bags & Gear
    {
        "product_id": 94,
        "product_name": "MSR Hubba Hubba 2-Person Lightweight Backpacking Tent with DuraShield Waterproofing",
        "aisle_id": 703, "department_id": 7, "price": 479.95, "rating": 4.8, "review_count": 920,
        "brand": "MSR",
        "description": "Weighs only 2 lbs 14 oz packed. True rectangular floorplan with 40-inch peak headroom, Easton Syclone aerospace composite poles virtually indestructible in mountain gusts, DuraShield waterproof polyurethane and silicone coated fly, two large StayDry vestibules."
    },
    {
        "product_id": 95,
        "product_name": "Sea to Summit Spark Ultralight Down 28°F (-2°C) Sleeping Bag 850+ Loft RDS Goose Down",
        "aisle_id": 703, "department_id": 7, "price": 399.00, "rating": 4.8, "review_count": 480,
        "brand": "Sea to Summit",
        "description": "Featherweight 17.4 oz mummy sleeping bag packed with premium 850+ fill power goose down treated with ULTRA-DRY water repellent down treatment eliminating condensation clumping, 10D nylon shell, contoured mummy fit maximizes thermal efficiency."
    },

    # Aisle 704: Hydration Bottles, Flasks & Coolers
    {
        "product_id": 96,
        "product_name": "Hydro Flask 32 oz Wide Mouth Vacuum Insulated Stainless Steel Water Bottle with Flex Straw Cap",
        "aisle_id": 704, "department_id": 7, "price": 44.95, "rating": 4.8, "review_count": 8200,
        "brand": "Hydro Flask",
        "description": "TempShield double-wall vacuum insulation keeps ice water ice-cold for up to 24 hours or hot beverages steaming for 12 hours, durable 18/8 pro-grade stainless steel construction eliminates flavor transfer, leakproof flex straw cap, dishwasher safe Color Last powder coat."
    },
    {
        "product_id": 97,
        "product_name": "YETI Tundra 45 Hard Cooler Heavy-Duty Rotomolded Ice Chest - Desert Tan",
        "aisle_id": 704, "department_id": 7, "price": 325.00, "rating": 4.9, "review_count": 5100,
        "brand": "YETI",
        "description": "Indestructible rotomolded construction armored to the core, up to 3 inches of PermaFrost polyurethane pressure-injected insulation in the walls and lid keeps ice frozen for days in scorching heat, Interagency Grizzly Bear Committee certified bear-resistant."
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 8. BEAUTY, SKINCARE & SUN CARE (Dept 8)
    # [COMPREHENSIVE SUN CARE SUITE WITH WET SKIN, SPORT, MINERAL, CHEMICAL SPECS]
    # ══════════════════════════════════════════════════════════════════════════
    # Aisle 801: Sun Care & Sunscreens (Wet Skin, Sport, Mineral & Chemical)
    {
        "product_id": 98,
        "product_name": "Neutrogena Wet Skin Kids Waterfull Sunscreen Spray Broad Spectrum SPF 70+ (Cuts Through Water)",
        "aisle_id": 801, "department_id": 8, "price": 13.99, "rating": 4.8, "review_count": 4320,
        "brand": "Neutrogena",
        "description": "Engineered with patented Helioplex technology specifically formulated to be applied directly onto wet skin or dry skin without dripping, whitening, or wiping off. Cuts straight through water molecules to bind securely to skin creating a continuous, water-resistant protective barrier for 80 minutes. Broad-spectrum UVA/UVB SPF 70+ protection, oil-free, PABA-free, and pediatrician-tested for active kids at pools and beaches."
    },
    {
        "product_id": 99,
        "product_name": "Neutrogena Wet Skin Sunscreen Stick Broad Spectrum SPF 70+ for Face & Body (Wet Skin Formula)",
        "aisle_id": 801, "department_id": 8, "price": 11.49, "rating": 4.7, "review_count": 2890,
        "brand": "Neutrogena",
        "description": "Hands-free, pocket-sized solid sunscreen stick featuring Helioplex Wet Skin technology. Glides effortlessly onto damp, soaking wet, or dry skin without slipping off or leaving white residue. Broad spectrum SPF 70+ protection against sunburn and premature aging, 80 minutes water-resistant, non-comedogenic (won't clog pores), ideal for face, ears, nose, and on-the-go water sports."
    },
    {
        "product_id": 100,
        "product_name": "Shiseido Ultimate Sun Protector Lotion SPF 50+ with SynchroShield WetForce & HeatForce Tech",
        "aisle_id": 801, "department_id": 8, "price": 50.00, "rating": 4.9, "review_count": 2180,
        "brand": "Shiseido",
        "description": "Breakthrough invisible sunscreen powered by SynchroShield technology: WetForce tech makes the UV protective veil significantly stronger when encountering water or sweat, while HeatForce tech strengthens the shield under intense sun heat. 80-minute water resistance, ocean-friendly formula free of oxybenzone and octinoxate, enriched with antioxidant skincare botanicals, invisible finish on all skin tones."
    },
    {
        "product_id": 101,
        "product_name": "La Roche-Posay Anthelios Melt-in Milk Sunscreen SPF 60 with Cell-Ox Shield Broad Spectrum",
        "aisle_id": 801, "department_id": 8, "price": 37.99, "rating": 4.8, "review_count": 5940,
        "brand": "La Roche-Posay",
        "description": "Award-winning face and body sunscreen lotion formulated with Cell-Ox Shield technology combining photostable broad-spectrum UVA/UVB filters with potent Senna Alata antioxidant defense against free radicals. Fast-absorbing, velvety melt-in texture leaves skin soft and hydrated without greasy film, water-resistant up to 80 minutes, dermatologist-tested for sensitive skin, fragrance-free, paraben-free."
    },
    {
        "product_id": 102,
        "product_name": "EltaMD UV Clear Broad-Spectrum SPF 46 Facial Sunscreen with Zinc Oxide & Niacinamide",
        "aisle_id": 801, "department_id": 8, "price": 43.00, "rating": 4.9, "review_count": 9800,
        "brand": "EltaMD",
        "description": "The gold-standard dermatologist-recommended facial sunscreen for sensitive, acne-prone, rosacea, and hyperpigmentation-prone skin. Contains 9.0% transparent Zinc Oxide for mineral physical UV deflection, combined with 5% high-purity Niacinamide (Vitamin B3) to calm redness, Hyaluronic Acid for weightless hydration, and Lactic Acid. Oil-free, fragrance-free, leaves zero white residue."
    },
    {
        "product_id": 103,
        "product_name": "Supergoop! Unseen Sunscreen Broad Spectrum SPF 40 Invisible Weightless Makeup Primer",
        "aisle_id": 801, "department_id": 8, "price": 38.00, "rating": 4.7, "review_count": 6700,
        "brand": "Supergoop!",
        "description": "100% invisible, weightless, scentless daily sunscreen gel with a velvety primer finish. Broad spectrum chemical SPF 40 filters protect against UVA, UVB, blue light, and infrared radiation. Formulated with red algae extract and meadowfoam seed oil to lock in hydration without shine. Water and sweat-resistant for 40 minutes, perfect under foundation or worn solo."
    },
    {
        "product_id": 104,
        "product_name": "Biore UV Aqua Rich Watery Essence SPF 50+ PA++++ Japanese Micro Defense Sunscreen",
        "aisle_id": 801, "department_id": 8, "price": 14.50, "rating": 4.8, "review_count": 7600,
        "brand": "Biore",
        "description": "World-famous Japanese sunscreen with World's First Micro Defense formula providing microscopic even coverage at 0.2-micron scale. Water capsule texture bursts into refreshing liquid upon contact with skin. Infused with Hyaluronic Acid, Royal Jelly Extract, and BG moisture components. Water-resistant for 80 minutes yet washes off easily with normal soap, zero stickiness or white cast."
    },
    {
        "product_id": 105,
        "product_name": "Sun Bum Original SPF 50 Sunscreen Spray Vegan Reef Friendly with Vitamin E (80 Min Water Resistant)",
        "aisle_id": 801, "department_id": 8, "price": 18.49, "rating": 4.7, "review_count": 3890,
        "brand": "Sun Bum",
        "description": "Classic moisturizing sunscreen spray with signature sweet coconut beach scent. Enriched with Vitamin E antioxidant to neutralize skin-damaging free radicals. Continuous ultra-fine mist sprays at any angle, water-resistant for 80 minutes. Reef friendly (Hawaii Act 104 compliant, no Oxybenzone or Octinoxate), vegan, gluten-free, paraben-free."
    },
    {
        "product_id": 106,
        "product_name": "Thinksport Safe Sunscreen Broad Spectrum SPF 50+ Non-Nano Zinc Oxide Sports Formula",
        "aisle_id": 801, "department_id": 8, "price": 16.99, "rating": 4.8, "review_count": 4200,
        "brand": "Thinksport",
        "description": "Top-rated non-toxic mineral sunscreen featuring 20% non-nano Zinc Oxide for immediate physical broad-spectrum UVA/UVB defense. Highest water-resistance rating of 80 minutes, EWG verified #1 top rating since 2010, Leaping Bunny certified cruelty-free, biological coral reef safe, fast-absorbing without harsh chemical smell."
    },
    {
        "product_id": 107,
        "product_name": "Blue Lizard Australian Sunscreen Sensitive Mineral SPF 50+ with Smart UV Bottle Cap",
        "aisle_id": 801, "department_id": 8, "price": 15.98, "rating": 4.8, "review_count": 5100,
        "brand": "Blue Lizard",
        "description": "Australian mineral formula with Zinc Oxide and Titanium Dioxide providing broad-spectrum coverage without chemical active filters, parabens, or fragrances. Smart bottle cap turns vibrant blue when harmful UV rays are present, reminding you to apply. 80-minute water and sweat resistant, trusted by pediatricians."
    },
    {
        "product_id": 108,
        "product_name": "Skin1004 Madagascar Centella Hyalu-Cica Water-Fit Sun Serum SPF 50+ PA++++ Korean Sunscreen",
        "aisle_id": 801, "department_id": 8, "price": 16.00, "rating": 4.9, "review_count": 6800,
        "brand": "Skin1004",
        "description": "Beloved Korean daily chemical sunscreen serum featuring Madagascar Centella Asiatica extract combined with Hyaluronic Acid to simultaneously soothe irritation and infuse deep moisture. Weightless lotion texture absorbs instantly leaving glowing, non-greasy dewy skin with zero white cast and no eye sting."
    },
    {
        "product_id": 109,
        "product_name": "Beauty of Joseon Relief Sun: Rice + Probiotics SPF 50+ PA++++ Organic Sunscreen",
        "aisle_id": 801, "department_id": 8, "price": 17.00, "rating": 4.9, "review_count": 9200,
        "brand": "Beauty of Joseon",
        "description": "Viral Korean facial sunscreen formulated with 30% Rice Extract and fermented Grain Probiotics rich in Vitamins B, C, and E. Delivers intensive nourishment and moisture barrier reinforcement while shielding against UV rays. Silky cream consistency glides like a gentle moisturizer without pilling under makeup."
    },
    {
        "product_id": 110,
        "product_name": "Coppertone Sport Continuous Sunscreen Spray SPF 50 High-Performance Water & Sweat Resistant",
        "aisle_id": 801, "department_id": 8, "price": 10.97, "rating": 4.7, "review_count": 3400,
        "brand": "Coppertone",
        "description": "Engineered for intense outdoor athletics, running, and swimming. Stays on strong through heavy sweat and water for 80 minutes without stinging eyes. Delivers continuous spray at any angle including upside-down, lightweight breathable feel, enriched with antioxidants."
    },
    {
        "product_id": 111,
        "product_name": "Hawaiian Tropic Island Sport Sunscreen Spray SPF 30 Breathable Ultra-Light Formula",
        "aisle_id": 801, "department_id": 8, "price": 11.29, "rating": 4.6, "review_count": 2100,
        "brand": "Hawaiian Tropic",
        "description": "Ultra-lightweight breathable sports sunscreen spray that won't clog pores or run into eyes during workouts. Sweat and water-resistant for 80 minutes, infused with island botanicals, plumeria flower extract, and iconic tropical coconut fragrance, PETA certified cruelty-free."
    },
    {
        "product_id": 112,
        "product_name": "Anessa Perfect UV Sunscreen Skincare Milk SPF 50+ PA++++ with Auto Booster Tech",
        "aisle_id": 801, "department_id": 8, "price": 32.00, "rating": 4.9, "review_count": 3100,
        "brand": "Shiseido Anessa",
        "description": "Japan's #1 sunscreen for 21 consecutive years. Features Auto Booster Technology that reacts to sweat, water, heat, and air humidity to strengthen the UV protective veil. Friction-proof, super waterproof for 80 minutes, infused with 50% skincare ingredients like collagen and green tea extract."
    },
    {
        "product_id": 113,
        "product_name": "Colorescience Total Eye 3-in-1 Renewal Therapy SPF 35 Mineral Eye Sunscreen & Dark Circle Concealer",
        "aisle_id": 801, "department_id": 8, "price": 79.00, "rating": 4.8, "review_count": 1850,
        "brand": "Colorescience",
        "description": "100% mineral SPF 35 sunscreen (Titanium Dioxide and Zinc Oxide) clinically proven to improve dark circles, puffiness, fine lines, and wrinkles around the delicate orbital eye area. Cooling applicator tip soothes tired eyes, natural tint conceals imperfections."
    },

    # Aisle 802: Facial Cleansers, Exfoliators & Toners
    {
        "product_id": 114,
        "product_name": "CeraVe Hydrating Facial Cleanser with Ceramides & Hyaluronic Acid for Normal to Dry Skin",
        "aisle_id": 802, "department_id": 8, "price": 15.99, "rating": 4.8, "review_count": 8900,
        "brand": "CeraVe",
        "description": "Non-foaming lotion cleanser formulated with 3 essential ceramides (1, 3, 6-II) and hyaluronic acid using patented MVE Delivery Technology to slowly release moisturizers all day, gently washes away dirt and oil without stripping moisture barrier."
    },
    {
        "product_id": 115,
        "product_name": "Paula's Choice Skin Perfecting 2% BHA Liquid Salicylic Acid Exfoliant for Blackheads & Pores",
        "aisle_id": 802, "department_id": 8, "price": 35.00, "rating": 4.8, "review_count": 9400,
        "brand": "Paula's Choice",
        "description": "Cult-favorite leave-on liquid exfoliant with 2% Salicylic Acid (BHA) that penetrates deep inside pores to clear dead skin buildup, dissolve excess sebum, unclog blackheads, shrink enlarged pores, and even skin tone with soothing green tea."
    },

    # Aisle 803: Targeted Serums (Vitamin C, Niacinamide, Retinol)
    {
        "product_id": 116,
        "product_name": "SkinCeuticals C E Ferulic Combination Antioxidant Serum 15% Pure L-Ascorbic Acid",
        "aisle_id": 803, "department_id": 8, "price": 182.00, "rating": 4.9, "review_count": 3400,
        "brand": "SkinCeuticals",
        "description": "Patented triple antioxidant formulation: 15% pure L-Ascorbic Acid (Vitamin C), 1% Alpha Tocopherol (Vitamin E), and 0.5% Ferulic Acid. Clinically proven to reduce combined oxidative damage from free radicals generated by UV, ozone, and pollution by up to 41%, improves firmness and brightens skin."
    },
    {
        "product_id": 117,
        "product_name": "The Ordinary Niacinamide 10% + Zinc 1% Oil Control & Blemish Serum 60ml",
        "aisle_id": 803, "department_id": 8, "price": 10.80, "rating": 4.7, "review_count": 8100,
        "brand": "The Ordinary",
        "description": "High-strength vitamin and mineral blemish formula with 10% pure Niacinamide to balance visible sebum activity and minimize pore congestion, backed by 1% Zinc PCA to calm redness and prevent oil buildup."
    },

    # Aisle 804: Barrier Moisturizers, Creams & Lip Care
    {
        "product_id": 118,
        "product_name": "Skinfix Barrier+ Triple Lipid-Peptide Cream Deep Hydration for Compromised Skin Barriers",
        "aisle_id": 804, "department_id": 8, "price": 54.00, "rating": 4.8, "review_count": 2400,
        "brand": "Skinfix",
        "description": "Clinically proven barrier-restoring moisturizer formulated with patented 3% Triple Lipid Complex mimicking the skin's natural lipid ratio (ceramides, cholesterol, free fatty acids), combined with 3% Nutripeptide blend and 1% soothing colloidal oatmeal."
    },
    {
        "product_id": 119,
        "product_name": "Laneige Lip Sleeping Mask Intense Hydration with Berry Fruit Complex & Murumuru Butter",
        "aisle_id": 804, "department_id": 8, "price": 24.00, "rating": 4.8, "review_count": 8900,
        "brand": "Laneige",
        "description": "Leave-on overnight lip treatment featuring Moisture Wrap technology, antioxidant Berry Fruit Complex rich in Vitamin C, coconut oil, shea butter, and murumuru seed butter, dissolves dry flakiness while delivering deep plumping moisture."
    },

    # Aisle 805: Luxury Haircare, Shampoos & Styling Tools
    {
        "product_id": 120,
        "product_name": "Dyson Supersonic Nural Intelligent Hair Dryer with Scalp Protect Sensor & Fast Drying",
        "aisle_id": 805, "department_id": 8, "price": 499.99, "rating": 4.8, "review_count": 1640,
        "brand": "Dyson",
        "description": "Equipped with Time of Flight sensors measuring distance to automatically reduce heat to 131°F near the scalp to prevent burning, capsule illumination lights showing current temperature, attachment learning recognizing styled preferences, V9 digital motor."
    },
    {
        "product_id": 121,
        "product_name": "Olaplex No. 3 Hair Perfector Repairing Treatment for Damaged & Bleached Hair",
        "aisle_id": 805, "department_id": 8, "price": 30.00, "rating": 4.8, "review_count": 9200,
        "brand": "Olaplex",
        "description": "Patented Bis-Aminopropyl Diglycol Dimaleate active bond building technology relinks broken disulfide bonds caused by chemical bleaching, heat tools, and mechanical brushing, restoring hair strength, texture, and shine."
    },

    # Aisle 806: Fragrances, Body Washes & Personal Care
    {
        "product_id": 122,
        "product_name": "Maison Francis Kurkdjian Baccarat Rouge 540 Eau de Parfum 70ml (Floral Amber Cedar)",
        "aisle_id": 806, "department_id": 8, "price": 325.00, "rating": 4.9, "review_count": 2100,
        "brand": "Maison Francis Kurkdjian",
        "description": "Luminous and sophisticated eau de parfum laying on skin like an amber floral and woody breeze. Aerial notes of jasmine and the radiance of saffron carry mineral facets of ambergris and woody tones of freshly cut cedar."
    },
    {
        "product_id": 123,
        "product_name": "Nécessaire The Body Wash Multi-Vitamin Daily Cleanser with Niacinamide - Eucalyptus",
        "aisle_id": 806, "department_id": 8, "price": 28.00, "rating": 4.7, "review_count": 3100,
        "brand": "Nécessaire",
        "description": "Daily multivitamin gel cleanser formulated with Niacinamide (Vitamin B3), Vitamin C, Vitamin E, Omega-6, and Omega-9, gently cleanses and nourishes body skin barrier, pure eucalyptus essential oil scent turns shower into a spa steam room."
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 9. GOURMET, COFFEE & HEALTH NUTRITION (Dept 9)
    # ══════════════════════════════════════════════════════════════════════════
    # Aisle 901: Whey Protein, Plant Protein & Bars
    {
        "product_id": 124,
        "product_name": "Optimum Nutrition Gold Standard 100% Whey Protein Powder 5 lbs - Double Rich Chocolate",
        "aisle_id": 901, "department_id": 9, "price": 84.99, "rating": 4.8, "review_count": 9800,
        "brand": "Optimum Nutrition",
        "description": "The world's bestselling whey protein. 24g of protein per serving with Whey Protein Isolate as primary source, 5.5g naturally occurring BCAAs, 4g glutamine & glutamic acid, instantized for effortless clump-free spoon stirring."
    },
    {
        "product_id": 125,
        "product_name": "Ghost 100% Vegan Plant Protein Powder 2 lbs - Cinnabon Cinnamon Roll Flavor",
        "aisle_id": 901, "department_id": 9, "price": 44.99, "rating": 4.8, "review_count": 2100,
        "brand": "Ghost",
        "description": "100% transparent label combining Pea Protein Concentrate, Organic Pumpkin Protein, and Watermelon Seed Protein, delivering 20g vegan protein with mouthwatering authentic Cinnabon bakery taste, soy-free and gluten-free."
    },

    # Aisle 902: Specialty Whole Bean Coffee & Ceremonial Matcha
    {
        "product_id": 126,
        "product_name": "Stumptown Coffee Roasters Hair Bender Whole Bean Coffee 12 oz (Sweet, Complex & Balanced)",
        "aisle_id": 902, "department_id": 9, "price": 16.99, "rating": 4.8, "review_count": 3400,
        "brand": "Stumptown",
        "description": "Stumptown's most celebrated blend crafted from coffees sourced from Latin America, Indonesia, and East Africa, featuring complex flavor notes of sweet dark chocolate, sweet orange citrus, and warm toffee."
    },
    {
        "product_id": 127,
        "product_name": "Ippodo Tea Sayaka First-Harvest Ceremonial Grade Japanese Uji Matcha 40g Tin",
        "aisle_id": 902, "department_id": 9, "price": 38.00, "rating": 4.9, "review_count": 1820,
        "brand": "Ippodo Tea",
        "description": "Authentic ceremonial matcha stone-ground in Kyoto, Japan by a 300-year-old tea house. Vibrant emerald green color, delicate balance of rich umami savory depth with gentle natural sweetness and zero bitterness."
    },

    # Aisle 903: Electrolytes, Energy Drinks & Hydration
    {
        "product_id": 128,
        "product_name": "LMNT Zero-Sugar Keto Electrolyte Drink Mix Variety Pack (30 Packets)",
        "aisle_id": 903, "department_id": 9, "price": 45.00, "rating": 4.9, "review_count": 5200,
        "brand": "LMNT",
        "description": "Science-backed electrolyte ratio containing 1000mg Sodium, 200mg Potassium, and 60mg Magnesium per packet with zero sugar, zero artificial ingredients, and zero fillers. Ideal for fasting, low-carb, keto, endurance runners, and hot yoga."
    },
    {
        "product_id": 129,
        "product_name": "Liquid I.V. Hydration Multiplier Electrolyte Powder Drink Mix 16 Sticks - Lemon Lime",
        "aisle_id": 903, "department_id": 9, "price": 24.99, "rating": 4.7, "review_count": 8400,
        "brand": "Liquid I.V.",
        "description": "Cellular Transport Technology (CTT) harnesses specific ratio of sodium, potassium, and glucose to deliver rapid hydration 2x faster into the bloodstream than plain water alone, packed with 5 essential vitamins (B3, B5, B6, B12, Vitamin C)."
    },

    # Aisle 904: Artisan Chocolates, Honey & Healthy Pantry
    {
        "product_id": 130,
        "product_name": "Manuka Health Raw MGO 400+ / UMF 13+ Certified Genuine New Zealand Manuka Honey 500g",
        "aisle_id": 904, "department_id": 9, "price": 59.99, "rating": 4.9, "review_count": 2700,
        "brand": "Manuka Health",
        "description": "100% pure raw unpasteurized Manuka honey harvested from remote pristine New Zealand bush, tested and certified to contain at least 400mg/kg naturally occurring Methylglyoxal (MGO) providing potent bioactive immune and gut wellness support."
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 10. BOOKS & PREMIUM STATIONERY (Dept 10)
    # ══════════════════════════════════════════════════════════════════════════
    # Aisle 1001: Bestselling Sci-Fi, Fantasy & Fiction
    {
        "product_id": 131,
        "product_name": "Dune by Frank Herbert (Deluxe Hardcover Collector's Edition with Stained Edges & Map)",
        "aisle_id": 1001, "department_id": 10, "price": 28.00, "rating": 4.9, "review_count": 8900,
        "brand": "Ace Books",
        "description": "The monumental science fiction epic set on the desert planet Arrakis. Deluxe clothbound hardcover edition featuring foil-stamped cover, dyed page edges, custom illustrated endpapers, and detailed maps of Arrakis ecology."
    },
    {
        "product_id": 132,
        "product_name": "Project Hail Mary by Andy Weir (Hardcover Novel - From the Author of The Martian)",
        "aisle_id": 1001, "department_id": 10, "price": 22.49, "rating": 4.9, "review_count": 7800,
        "brand": "Ballantine Books",
        "description": "Thrilling interstellar science survival adventure following solitary astronaut Ryland Grace as he awakens aboard a spaceship with amnesia to discover humanity faces extinction from solar-dimming Astrophage microorganisms."
    },

    # Aisle 1002: Technology, Productivity & Leadership Books
    {
        "product_id": 133,
        "product_name": "Atomic Habits by James Clear (Hardcover - Tiny Changes, Remarkable Results)",
        "aisle_id": 1002, "department_id": 10, "price": 18.00, "rating": 4.9, "review_count": 18900,
        "brand": "Avery Publishing",
        "description": "The definitive #1 New York Times bestselling practical guide on habit formation, the Four Laws of Behavior Change, environment architecture, identity-based habits, and harnessing 1% daily marginal gains to reshape your life."
    },
    {
        "product_id": 134,
        "product_name": "Deep Work: Rules for Focused Success in a Distracted World by Cal Newport (Hardcover)",
        "aisle_id": 1002, "department_id": 10, "price": 19.99, "rating": 4.8, "review_count": 6200,
        "brand": "Grand Central Publishing",
        "description": "Provocative guide arguing that the ability to focus without distraction on cognitively demanding tasks is becoming extraordinarily rare and simultaneously massively valuable in the modern knowledge economy."
    },

    # Aisle 1003: Fountain Pens, Dot-Grid Journals & Desk Tech
    {
        "product_id": 135,
        "product_name": "Pilot Custom 823 Fountain Pen - Amber Barrel with 14K Gold Nib & Vacuum Filler",
        "aisle_id": 1003, "department_id": 10, "price": 336.00, "rating": 4.9, "review_count": 840,
        "brand": "Pilot",
        "description": "Exquisite Japanese luxury writing instrument with translucent amber resin barrel, massive 14-karat gold #15 nib providing buttery smooth line flow, high-capacity vacuum plunger filling system holding over 2.5ml ink."
    },
    {
        "product_id": 136,
        "product_name": "Leuchtturm1919 Hardcover Medium A5 Dot-Grid Notebook (Numbered Pages & Table of Contents)",
        "aisle_id": 1003, "department_id": 10, "price": 24.50, "rating": 4.8, "review_count": 6400,
        "brand": "Leuchtturm1919",
        "description": "Premium German journaling notebook featuring 251 numbered pages of 80gsm ink-proof, acid-free paper, blank table of contents, 8 perforated detachable sheets, expandable back pocket, dual page markers, and elastic closure band."
    },
]

# We will programmatically generate additional rich, category-specific items
# to bring the total database size to 320+ items across all categories!

extra_items = []
current_id = 137

# Function to generate extra structured items per aisle
def add_product(name, aisle_id, dept_id, price, rating, reviews, brand, desc):
    global current_id
    extra_items.append({
        "product_id": current_id,
        "product_name": name,
        "aisle_id": aisle_id,
        "department_id": dept_id,
        "price": round(price, 2),
        "rating": round(rating, 1),
        "review_count": reviews,
        "brand": brand,
        "description": desc
    })
    current_id += 1

# Additional Sun Care & Skin Care (ensuring total coverage of wet skin / sun queries)
add_product("Neutrogena Hydro Boost Water Gel Sunscreen Broad Spectrum SPF 50 Hyaluronic Acid", 801, 8, 14.99, 4.7, 3400, "Neutrogena", "Water-light gel sunscreen infused with hyaluronic acid, quenching dry skin with weightless hydration, oil-free, non-comedogenic, 80 min water resistant.")
add_product("Badger Damascus Rose Mineral Face Sunscreen SPF 30 Clear Zinc Oxide Reef-Safe", 801, 8, 17.99, 4.6, 980, "Badger", "100% certified natural organic sun care with clear non-nano zinc oxide, soothing damascus rose and seabuckthorn, water resistant 40 minutes, biodegradable.")
add_product("Round Lab Birch Juice Moisturizing Sunscreen SPF 50+ PA++++ Cooling Hyaluronic Sun Gel", 801, 8, 18.00, 4.9, 5400, "Round Lab", "Korean Holy Grail sunscreen formulated with Inje Birch Tree Sap and Vita Hyaluronic Acid to hydrate and cool overheated skin, zero white cast, certified reef safe.")
add_product("Isntree Hyaluronic Acid Watery Sun Gel SPF 50+ PA++++ with 8 Types of Hyaluronic Acid", 801, 8, 16.50, 4.8, 4100, "Isntree", "Centella asiatica, astaxanthin, and eight molecular weights of hyaluronic acid combine to replenish moisture barrier while defending against UV rays, lightweight gel.")
add_product("Coola Organic Classic Face Sunscreen SPF 50 Fragrance-Free 70%+ Organic Antioxidant", 801, 8, 32.00, 4.7, 1850, "Coola", "Farm-to-face organic antioxidant Plant Protection complex shields skin against free radicals, lightweight sheer lotion, 80 minutes water resistant, Hawaii reef compliant.")
add_product("Supergoop! Glowscreen Broad Spectrum SPF 40 Hydrating Dewy Makeup Primer with Niacinamide", 801, 8, 38.00, 4.7, 4300, "Supergoop!", "Illuminating tinted sunscreen that gives instant dewy, pearlescent glow while delivering broad spectrum SPF 40 and blue light protection with hyaluronic acid and vitamin B5.")
add_product("Banana Boat Sport Ultra Sunscreen Spray SPF 50 High Endurance Water & Sweat Resistant", 801, 8, 9.98, 4.6, 3100, "Banana Boat", "Clinically proven sport endurance protection that stays on through seven conditions: sun, pool water, ocean water, wind, sweat, sand, and 100-degree heat, 80 min water resistant.")
add_product("Sun Bum Mineral SPF 50 Sunscreen Lotion Non-Nano Zinc Oxide Vegan Hypoallergenic", 801, 8, 16.99, 4.6, 2100, "Sun Bum", "Zinc-based physical sunscreen lotion providing sheer matte mineral finish without chemical actives, water resistant 80 minutes, fragrance-free for sensitive skin.")

# Additional Laptops & Electronics
add_product("Dell XPS 13 9340 Ultralight Laptop (Intel Core Ultra 7 155H, 16GB RAM, 512GB SSD) Platinum", 201, 2, 1299.99, 4.7, 850, "Dell", "Sleek 2.6 lb aluminum laptop with edge-to-edge glass keyboard and seamless glass touchpad, 13.4-inch FHD+ 120Hz display, dual Thunderbolt 4 ports, 18 hour battery.")
add_product("Lenovo Legion Pro 7i Gen 9 Gaming Laptop (Intel Core i9-14900HX, RTX 4090 16GB, 32GB RAM, 2TB SSD)", 201, 2, 2999.99, 4.8, 410, "Lenovo", "Ultimate desktop-replacement powerhouse with Legion Coldfront vapor chamber cooling, 16-inch WQXGA 240Hz 500 nits gaming display, full-power 175W RTX 4090 GPU.")
add_product("Apple Mac Studio M2 Max (12-core CPU, 30-core GPU, 32GB Unified Memory, 512GB SSD)", 201, 2, 1999.00, 4.9, 620, "Apple", "Compact desktop powerhouse designed for professional music producers, video editors, and 3D animators, 4x Thunderbolt 4 ports, 10Gb Ethernet, whisper-quiet thermal design.")
add_product("LG gram 17 Super-Lightweight Laptop (Intel Core Ultra 7, 32GB RAM, 1TB SSD, 2.98 lbs)", 201, 2, 1699.99, 4.6, 530, "LG", "Full 17-inch IPS WQXGA (2560x1600) anti-glare display packed into an astonishingly light sub-3 lb magnesium alloy chassis, 80Wh battery lasting up to 20 hours.")
add_product("HP Spectre x360 14 2-in-1 Touchscreen Laptop OLED (Intel Core Ultra 7, 16GB RAM, 1TB SSD)", 201, 2, 1449.99, 4.7, 490, "HP", "Convertible laptop with 14-inch 2.8K 120Hz OLED touchscreen, 9MP AI camera with auto-framing, gem-cut aluminum chassis, bundled rechargeable MPP 2.0 tilt pen.")
add_product("Framework Laptop 16 Modular DIY Laptop (AMD Ryzen 7 7840HS, Expansion Bay GPU Modular)", 201, 2, 1799.00, 4.8, 310, "Framework", "Fully upgradeable, repairable modular laptop with hot-swappable ports, customizable keyboard matrix, removable discrete graphics module, and transparent sustainability.")

# Additional Audio & Sound
add_product("Bowers & Wilkins Px7 S2e Over-Ear Noise-Cancelling Headphones with 24-bit DSP", 301, 3, 399.00, 4.8, 410, "Bowers & Wilkins", "Audiophile wireless headphones with custom 40mm bio-cellulose drivers, 24-bit high-resolution digital signal processing, 6 microphones for crystal ANC, luxurious memory foam.")
add_product("Marshall Major IV On-Ear Wireless Bluetooth Headphones with 80+ Hours Playtime", 301, 3, 149.99, 4.7, 3100, "Marshall", "Iconic textured vinyl and brass script design, custom-tuned dynamic drivers, multi-directional brass control knob, wireless Qi charging, collapsible travel design.")
add_product("Nothing Ear (a) True Wireless Earbuds with Smart ANC and ChatGPT Voice Integration", 302, 3, 99.00, 4.6, 1200, "Nothing", "Striking transparent yellow aesthetic, 11mm ceramic driver, 45dB Smart ANC with real-time leak detection, Hi-Res LDAC audio, integrated ChatGPT pinch-to-talk voice assistant.")
add_product("JBL Flip 6 Waterproof Portable Bluetooth Speaker IP67 2-Way Speaker System", 303, 3, 129.95, 4.8, 8900, "JBL", "Racetrack-shaped woofer, separate tweeter, and dual passive radiators delivering punchy loud bass, IP67 waterproof and dustproof, 12 hours playtime, PartyBoost linking.")
add_product("Sonos Move 2 Heavy-Duty Weatherproof Portable Smart Speaker with Stereo Sound & 24h Battery", 303, 3, 449.00, 4.8, 890, "Sonos", "Room-filling stereo acoustics with dual angled tweeters and precision woofer, IP56 weather resistance against rain and dust, automatic Trueplay tuning, 24 hours playback.")
add_product("Bose SoundLink Flex Bluetooth Speaker (2nd Gen) IP67 Waterproof & PositionIQ Tech", 303, 3, 149.00, 4.8, 3400, "Bose", "PositionIQ technology automatically optimizes audio whether standing upright, flat on back, or hanging, waterproof and dustproof (IP67), resists drops and rust.")

# Additional Kitchen & Home Appliances
add_product("Breville Smart Oven Air Fryer Pro Convection Countertop Oven with Element iQ", 402, 4, 399.95, 4.8, 3800, "Breville", "Super Convection technology with 2-speed fan, 13 cooking functions including proof, slow cook, dehydrate, and air fry, fits 9-slice bread or a 14-lb turkey, LCD display.")
add_product("Fellow Stagg EKG Electric Gooseneck Pour-Over Kettle with Variable Temp Control 0.9L", 401, 4, 165.00, 4.9, 4200, "Fellow", "Barista-standard precision pour gooseneck spout, to-the-degree PID temperature control from 135°F to 212°F, 60-minute temperature hold mode, high-contrast LCD screen.")
add_product("Instant Pot Pro 10-in-1 Pressure Cooker 6-Quart with Easy-Release Steam Valve", 402, 4, 169.95, 4.8, 6700, "Instant Pot", "Upgraded inner pot with stay-cool silicone handles safe for stovetops, 20% faster heating, gentle quiet steam release switch, 28 customizable cooking programs.")
add_product("KitchenAid Artisan Series 5-Quart Tilt-Head Stand Mixer - Empire Red", 403, 4, 449.99, 4.9, 9800, "KitchenAid", "Iconic American kitchen centerpiece with 10 speeds, 59 touchpoints per rotation for thorough ingredient incorporation, stainless steel bowl with comfortable handle.")
add_product("Anova Precision Cooker 3.0 Sous Vide Machine with Dual Band Wi-Fi & Touchscreen", 402, 4, 199.00, 4.7, 2400, "Anova Culinary", "Cooks food to exact internal temperature within 0.1°F, 1100 watts of power heating water rapidly, Bluetooth & dual-band Wi-Fi control via iOS/Android recipe app.")
add_product("iRobot Roomba Combo j9+ Self-Emptying & Auto-Refill Robot Vacuum and Retractable Mop", 404, 4, 999.00, 4.6, 1200, "iRobot", "D.R.I.V.E. retractable mop arm lifts mop pads to top of vacuum to keep carpets 100% dry, Clean Base auto-fills liquid for 30 days and empties dust for 60 days, pet waste guarantee.")
add_product("Shark Stratos Cordless Vacuum with Clean Sense IQ & DuoClean PowerFins HairPro", 404, 4, 449.99, 4.7, 1980, "Shark", "Clean Sense IQ detects invisible dirt and automatically boosts power, dual brushrolls grab hair without tangling, MultiFLEX folding wand reaches under low furniture.")
add_product("Coway Airmega 400 Smart True HEPA Air Purifier for 1,560 sq ft with Max2 Filter", 405, 4, 499.00, 4.8, 2800, "Coway", "Dual suction draws air from both sides, combined Green True HEPA and activated carbon filter eliminates 99.99% of airborne particles and VOC gases, smart eco-mode.")
add_product("Blueair Blue Pure 211+ Auto Air Purifier with Washable Fabric Pre-Filter", 405, 4, 299.99, 4.8, 4100, "Blueair", "HEPASilent filtration technology cleans 540 sq ft room in just 12.5 minutes while using less energy than a single lightbulb, one-button auto mode with air quality LED.")

# Additional Footwear & Running Shoes
add_product("Asics Gel-Kayano 31 Maximum Support Stability Running Shoes for Overpronation", 601, 6, 165.00, 4.8, 3800, "Asics", "4D GUIDANCE SYSTEM adapts to foot movement for revolutionary stability, FF BLAST PLUS ECO cushioning, PureGEL technology in heel provides 65% softer impact landings.")
add_product("Saucony Endorphin Speed 4 Nylon-Plated Tempo Training & Race Running Shoes", 601, 6, 170.00, 4.9, 2100, "Saucony", "Winged nylon plate delivers explosive energy return and lateral support, ultra-responsive PWRRUN PB peba foam, SPEEDROLL rocker technology drives effortless turnover.")
add_product("Altra Lone Peak 8 Zero Drop Trail Running Shoes with FootShape Toe Box", 601, 6, 140.00, 4.7, 2900, "Altra", "Natural FootShape spacious toe box allows toes to splay comfortably, balanced Zero Drop platform, MaxTrac sticky lug outsole, durable ripstop mesh trail upper.")
add_product("On Cloudmonster 2 Maximum Cushion Road Running Shoes with Helion Superfoam", 601, 6, 179.99, 4.7, 2400, "On Running", "Monster-level CloudTec cushioning absorbs heavy impacts, nylon-blend Speedboard shoots you forward with massive energy return, breathable engineered mesh upper.")
add_product("Hoka Speedgoat 5 Lightweight Vibram Megagrip Trail Running Shoes", 601, 6, 155.00, 4.8, 4100, "Hoka", "Trail icon equipped with Vibram Megagrip with Traction Lug for enhanced ground grip on loose dirt and rocky ridges, lightweight CMEVA midsole foam, protective toe rand.")

# Fill out 320+ products systematically across remaining aisles:
departments_map = {
    101: 1, 102: 1, 103: 1, 104: 1, 105: 1,
    201: 2, 202: 2, 203: 2, 204: 2, 205: 2,
    301: 3, 302: 3, 303: 3, 304: 3,
    401: 4, 402: 4, 403: 4, 404: 4, 405: 4,
    501: 5, 502: 5, 503: 5, 504: 5, 505: 5,
    601: 6, 602: 6, 603: 6, 604: 6,
    701: 7, 702: 7, 703: 7, 704: 7,
    801: 8, 802: 8, 803: 8, 804: 8, 805: 8, 806: 8,
    901: 9, 902: 9, 903: 9, 904: 9,
    1001: 10, 1002: 10, 1003: 10,
}

# Systematic additional item definitions
systematic_items = [
    # Electronics
    ("Anker 737 Power Bank (PowerCore 24K) 140W Two-Way Fast Charging", 105, 129.99, 4.8, 3800, "Anker", "Smart digital display power bank with 24,000mAh capacity and 140W ultra-powerful two-way charging."),
    ("Belkin BoostCharge Pro 3-in-1 Wireless Charging Pad with MagSafe 15W", 105, 149.99, 4.7, 1800, "Belkin", "Flat lay MagSafe charging pad for iPhone 15/16, fast charging Apple Watch Ultra, and AirPods case."),
    ("Tile Pro Powerful Bluetooth Item Tracker 400 ft Range Water-Resistant (2-Pack)", 104, 59.99, 4.6, 2800, "Tile", "High-range item finder with replaceable 1-year battery, loud ring volume, compatible with Android and iOS."),
    ("Nanoleaf Shapes Hexagons Smarter Kit (7 Light Panels) Modular RGB Lighting", 104, 199.99, 4.7, 1400, "Nanoleaf", "Ultra-thin modular LED smart light panels with Connect+ tech, music visualizer, Touch Actions, Apple HomeKit."),
    ("Garmin Venu 3 GPS Smartwatch with Bright AMOLED Display & Advanced Sleep Coach", 103, 449.99, 4.8, 1200, "Garmin", "Health and fitness watch with personalized sleep coach, nap detection, wheel chair mode, built-in mic and speaker."),
    ("Fitbit Charge 6 Fitness Tracker with Google Apps & Heart Rate on Gym Equipment", 103, 159.95, 4.5, 3400, "Fitbit", "Built-in GPS, YouTube Music controls, Google Maps directions, ECG app, EDA scan for stress management."),
    ("Amazon Fire Max 11 Tablet 64GB 11-inch 2.4 Million Pixel Display Octa-Core", 102, 229.99, 4.5, 2900, "Amazon", "Aluminum body tablet with vivid 2000x1200 screen, optional keyboard case and stylus, 14 hour battery life."),
    ("Kobo Libra Colour 7-inch Waterproof Color E-Reader with Stylus Support", 102, 219.99, 4.7, 850, "Kobo", "E Ink Kaleido 3 color screen, IPX8 waterproof, page turn buttons, compatible with Kobo Stylus 2 for markup."),

    # Computers & Gaming
    ("Samsung Odyssey OLED G9 49-inch Curved Dual QHD 240Hz 0.03ms Gaming Monitor", 202, 1199.99, 4.7, 890, "Samsung", "Ultrawide 32:9 Neo Quantum Processor OLED panel with 1800R curve, 240Hz refresh, AMD FreeSync Premium Pro."),
    ("BenQ PD3220U 32-inch 4K Thunderbolt 3 Designer Monitor with 100% sRGB & DCI-P3", 202, 1099.99, 4.7, 450, "BenQ", "DualView mode, KVM switch, factory calibrated color accuracy, hotkey puck for instant preset switching."),
    ("Xbox Series X 1TB Console 4K 120FPS Gaming with Velocity Architecture", 203, 499.99, 4.8, 6200, "Microsoft", "12 teraflops raw graphical processing power, DirectX ray tracing, Quick Resume between multiple games."),
    ("Sony PlayStation DualSense Edge Wireless Pro Controller for PS5", 203, 199.99, 4.7, 2400, "Sony", "Customizable back buttons, changeable stick caps, replaceable stick modules, adjustable trigger stops."),
    ("Corsair K70 MAX RGB Magnetic-Mechanical Gaming Keyboard with Adjustable Actuation", 204, 229.99, 4.7, 650, "Corsair", "CORSAIR MGX magnetic switches with customizable actuation from 0.4mm to 3.6mm, Rapid Trigger mode, aluminum."),
    ("SteelSeries Apex Pro TKL Wireless Mechanical Gaming Keyboard with OmniPoint 2.0", 204, 249.99, 4.7, 1100, "SteelSeries", "World's fastest keyboard with OmniPoint 2.0 magnetic switches, 20x faster actuation, OLED smart display."),
    ("SanDisk Professional 4TB PRO-BLADE Transport Modular SSD USB-C 2000MB/s", 205, 419.99, 4.8, 380, "SanDisk", "High-capacity modular external NVMe SSD with aluminum enclosure acting as heat sink for sustained 4K/8K capture."),
    ("OWC Thunderbolt 4 Hub 5-Port with 60W Power Delivery & 40Gbps Speed", 205, 149.99, 4.7, 720, "OWC", "Adds 3 Thunderbolt 4 ports and 1 USB-A port to Macs and PCs, daisy chain up to 5 Thunderbolt devices."),

    # Audio
    ("Marshall Acton III Bluetooth Home Speaker with Wide Stereo Soundstage - Black", 304, 279.99, 4.8, 1450, "Marshall", "Tweeters angled outwards and updated waveguides deliver consistently solid room-filling sound, brass dial controls."),
    ("JBL Bar 1300X 11.1.4-Channel Dolby Atmos Soundbar with Detachable Wireless Surrounds", 304, 1699.95, 4.8, 490, "JBL", "True 3D sound with detachable battery-powered wireless rear speakers and massive 12-inch wireless subwoofer."),
    ("Beats Studio Pro Wireless Noise Cancelling Over-Ear Headphones - Matte Black", 301, 349.99, 4.6, 2900, "Beats", "Custom 40mm acoustic platform with zero distortion, fully adaptive Active Noise Cancelling, USB-C lossless audio."),
    ("Shure AONIC 50 Gen 2 Premium Wireless Noise Cancelling Studio Headphones", 301, 349.00, 4.7, 510, "Shure", "Engineered from decades of stage experience, 50mm dynamic drivers, Snapdragon Sound with aptX Adaptive."),
    ("Sony LinkBuds S Truly Wireless Noise Cancelling Earbuds Ultra-Light 4.8g", 302, 199.99, 4.6, 3100, "Sony", "Never off smart sensing switches automatically between ambient sound and noise cancellation, LDAC codec."),
    ("JBL Tour Pro 2 True Wireless Earbuds with World's First Smart Touch Display Case", 302, 249.95, 4.5, 980, "JBL", "Control earbud settings, manage calls, playback, and equalizer directly from the 1.45-inch color touch case."),
    ("Anker Soundcore Motion 300 Hi-Res Wireless Outdoor Speaker with SmartTune", 303, 79.99, 4.7, 2400, "Anker Soundcore", "Wireless Hi-Res audio with LDAC, SmartTune orientation sensor adapts EQ, 30W stereo sound, IPX7 waterproof."),
    ("Bose SoundLink Max Portable Bluetooth Boombox Speaker with Deep Bass", 303, 399.00, 4.8, 620, "Bose", "Epic stereo sound with deep bass in a rugged portable carry design with soft rope handle, 20-hour battery life."),

    # Home & Kitchen
    ("Baratza Encore ESP Conical Burr Espresso and Filter Coffee Grinder", 401, 199.95, 4.8, 2600, "Baratza", "40mm M2 stainless steel conical burrs with micro-steps 1-20 for high-resolution espresso calibration."),
    ("Gaggia Classic Pro Manual Espresso Machine with Commercial Steam Wand (Made in Italy)", 401, 449.00, 4.7, 1850, "Gaggia", "Traditional commercial 58mm chrome-plated brass portafilter, 3-way solenoid valve, commercial two-hole steam wand."),
    ("Philips Premium Airfryer XXL with Fat Removal Technology 3-lb Capacity", 402, 249.95, 4.7, 3100, "Philips", "Twin TurboStar technology captures excess fat from meats while maintaining crispy skin and tender interior."),
    ("Cuisinart Custom 14-Cup Food Processor with Stainless Steel Blades", 402, 249.95, 4.8, 4800, "Cuisinart", "Heavy-duty 720-watt motor handles whole fruits, kneads pizza dough, and shreds cheeses effortlessly."),
    ("Staub Cast Iron 5.5-Qt Round Cocotte Dutch Oven - Matte Black (Made in France)", 403, 399.95, 4.9, 2100, "Staub", "Spike textured lid circulates continuous self-basting rainfall of moisture, black matte enamel interior."),
    ("Wüsthof Classic 8-inch Chef's Knife Forged High-Carbon Stainless Steel (Solingen Germany)", 403, 170.00, 4.9, 3900, "Wüsthof", "Precision forged from a single blank of high-carbon stainless steel with full tang and triple-riveted handle."),
    ("Lodge 10.25-inch Pre-Seasoned Cast Iron Skillet with Silicone Hot Handle Holder", 403, 29.90, 4.8, 9800, "Lodge", "Unmatched heat retention and even heating for searing steaks, baking cornbread, and camping fire pits."),
    ("Shark Matrix Plus 2-in-1 Robot Vacuum & Mop with Sonic Mopping & Self-Empty Base", 404, 499.99, 4.6, 2100, "Shark", "Matrix Clean uses precision grid pattern taking multiple passes over dirt, sonic mopping scrubs 100x/minute."),
    ("Dyson Ball Animal 3 Extra Upright Vacuum with De-tangling Motorbar for Pet Hair", 404, 499.99, 4.7, 2800, "Dyson", "Ball technology maneuvers smoothly around obstacles, de-tangling vanes clear hair automatically from brush bar."),
    ("Blueair Blue Pure 411a Max Air Purifier for Bedrooms and Home Offices (QuietMark)", 405, 139.99, 4.8, 3800, "Blueair", "Whisper quiet HEPASilent technology cleans 219 sq ft in 12.5 minutes, air quality indicator light, low energy."),

    # Fashion & Footwear
    ("Patagonia Better Sweater Fleece Jacket 100% Recycled Polyester Sweater-Knit", 502, 159.00, 4.8, 4100, "Patagonia", "Low-impact dyeing process significantly reduces dyestuffs and energy, soft fleece interior, zippered hand pockets."),
    ("Barbour Classic Beaufort Waxed Cotton Weatherproof Field Jacket - Olive", 501, 445.00, 4.9, 1100, "Barbour", "Traditional Sylkoil waxed 100% cotton resists rain and brambles, corduroy collar, classic tartan cotton lining."),
    ("Carhartt WIP Chase Heavyweight Cotton Sweatshirt Crewneck - Grey Heather", 502, 98.00, 4.7, 1400, "Carhartt WIP", "Durable cotton-poly fleece blend brushed for softness, ribbed collar, cuffs, and hem, gold logo embroidery."),
    ("Nudie Jeans Lean Dean Slim Tapered Organic Comfort Stretch Denim - Dry Cold Black", 503, 185.00, 4.7, 920, "Nudie Jeans", "100% organic cotton denim with subtle stretch, slim tapered silhouette, orange thread stitching, repair warranty."),
    ("Ten Thousand Interval Short 7-inch Workout Gym Athletic Shorts with Compression Liner", 504, 78.00, 4.8, 2300, "Ten Thousand", "Engineered for intense HIIT and lifting sessions, anti-chafe compression liner with dedicated phone pocket."),
    ("Patagonia Black Hole Duffel Bag 55L Weather-Resistant Recycled TPU Travel Pack", 505, 169.00, 4.9, 3900, "Patagonia", "Extremely tough 100% recycled polyester ripstop with weather-resistant matte TPU laminate, removable shoulder straps."),
    ("Topo Designs Rover Pack Classic 20L Water-Resistant Outdoor Heritage Backpack", 505, 99.00, 4.7, 1800, "Topo Designs", "1000D Cordura base with 420D nylon pack cloth, dual side water bottle pockets, cinch top closure with flap."),
    ("Hoka Clifton 9 Lightweight Daily Road Running Shoes for High Mileage Comfort", 601, 145.00, 4.8, 6200, "Hoka", "3mm more stack height with responsive new EVA foam, breathable engineered knit upper, early-stage Meta-Rocker."),
    ("Brooks Adrenaline GTS 23 Stability Running Shoes with GuideRails Holistic Support", 601, 140.00, 4.8, 5900, "Brooks", "GuideRails holistic support system keeps excess knee and ankle movement in check, DNA LOFT v2 plush cushioning."),
    ("Vans Old Skool Suede and Canvas Skate Sneaker - Classic Black/White", 602, 70.00, 4.8, 8900, "Vans", "Iconic side stripe skate shoe with durable suede and canvas uppers, reinforced toe caps, signature waffle outsoles."),
    ("Converse Chuck Taylor All Star 70 High Top Vintage Canvas Sneaker - Parchment", 602, 90.00, 4.8, 4800, "Converse", "Upgraded 12-oz heavy vintage canvas, winged tongue stitching, cushioned Ortholite insole, glossy egret foxing."),
    ("Danner Mountain Light Waterproof Full-Grain Leather Hiking Boots (Made in USA)", 603, 440.00, 4.9, 980, "Danner", "One-piece full-grain leather upper, 100% waterproof breathable GORE-TEX lining, Vibram Kletterlift outsole."),
    ("Keen Targhee III Mid Waterproof Breathable Leather Trail Hiking Boots", 603, 165.00, 4.7, 4500, "Keen", "KEEN.DRY waterproof membrane, all-terrain rubber outsole with 4mm multi-directional lugs, roomier toe box."),
    ("Crocs Classic Clog Slip-On Water-Friendly Lightweight Comfort Shoes - Slate Grey", 604, 49.99, 4.8, 9900, "Crocs", "Pivoting heel strap, ventilation ports shed water and debris rapidly, Croslite foam cushioning for all-day ease."),
    ("Birkenstock Boston Suede Leather Clogs with Contoured Cork Footbed - Taupe", 604, 160.00, 4.8, 5200, "Birkenstock", "Classic slip-on clog crafted from velvety suede, anatomically contoured natural cork-latex footbed."),

    # Sports & Outdoors
    ("Garmin Edge 840 Solar GPS Bike Computer with Adaptive Coaching & ClimbPro", 701, 499.99, 4.8, 840, "Garmin", "Power Glass solar charging lens adds up to 32 hours battery life, multi-band GNSS, targeted cycling ability coach."),
    ("Wahoo KICKR v6 Smart Indoor Bike Trainer with Direct Drive & Auto-Calibration", 701, 1299.99, 4.9, 610, "Wahoo", "Realistic road feel with up to 2200W resistance and 20% incline simulation, integrated Wi-Fi connection, ERG Easy Ramp."),
    ("Ironmaster Quick-Lock Adjustable Dumbbells System 75 lb Set with Stand", 702, 869.00, 4.9, 1200, "Ironmaster", "Indestructible welded steel construction, adjusts from 5 to 75 lbs, handles feel identical to solid gym dumbbells."),
    ("Lululemon The Mat 5mm Natural Rubber Reversible Grippy Yoga Mat", 702, 98.00, 4.7, 3400, "Lululemon", "Polyurethane top layer absorbs moisture for slip-free grip during sweaty Vinyasa, natural rubber base cushions hips."),
    ("Big Agnes Copper Spur HV UL2 Ultralight 2-Person Freestanding Backpacking Tent", 703, 549.95, 4.8, 790, "Big Agnes", "Award-winning double-wall ultralight tent weighing 2 lbs 11 oz with dual awning-style vestibules, proprietary nylon."),
    ("Nemo Disco 15 Sleeping Bag 650 Down Fill Spoon Shape for Side Sleepers", 703, 319.95, 4.8, 920, "NEMO", "Spoon shape contours provide room at elbows and knees for natural side sleeping, Thermo Gills regulate temperature."),
    ("Stanley Quencher H2.0 FlowState Stainless Steel Tumbler 40 oz with Straw - Cream", 704, 45.00, 4.8, 9800, "Stanley", "Double-wall vacuum insulation keeps ice cold for up to 48 hours, Comfort-grip handle, fits in car cup holders."),
    ("YETI Rambler 26 oz Straw Bottle Vacuum Insulated with Chug Cap - Navy", 704, 40.00, 4.9, 6400, "YETI", "18/8 stainless steel resists dents and drops, DoubleWall insulation keeps water cold until the last drop."),

    # Skincare & Beauty
    ("CeraVe PM Facial Moisturizing Lotion with Niacinamide and 3 Essential Ceramides", 804, 15.99, 4.8, 7800, "CeraVe", "Ultra-lightweight nighttime oil-free moisturizer with MVE delivery technology, restores protective skin barrier."),
    ("La Roche-Posay Effaclar Duo Acne Treatment with Benzoyl Peroxide & LHA", 803, 23.99, 4.7, 4200, "La Roche-Posay", "Dual action micronized Benzoyl Peroxide reduces acne blemishes in 3 days, micro-exfoliating Lipo-Hydroxy Acid."),
    ("COSRX Advanced Snail 96 Mucin Power Essence 100ml Repairing Hydration", 803, 25.00, 4.8, 9100, "COSRX", "Formulated with 96.3% Snail Secretion Filtrate to replenish moisture, repair damaged skin barriers, and fade dark spots."),
    ("Tatcha The Dewy Skin Cream Rich Plumping Moisturizer with Japanese Purple Rice", 804, 72.00, 4.8, 3800, "Tatcha", "Rich antioxidant-packed moisturizing cream with Japanese purple rice, Okinawa algae blend, and hyaluronic acid."),
    ("Kiehl's Ultra Facial Cream with Squalane 24-Hour Daily Deep Hydration", 804, 38.00, 4.8, 5400, "Kiehl's", "Glacial Glycoprotein and olive-derived Squalane provide 24-hour hydration even in extreme winter temperatures."),
    ("Moroccanoil Treatment Original Hair Oil with Argan Oil & Vitamin E (100ml)", 805, 48.00, 4.9, 8200, "Moroccanoil", "Pioneering argan oil infused conditioning treatment speeds up blow-drying time, detangles, and boosts brilliant shine."),
    ("K18 Leave-In Molecular Repair Hair Mask with Biomimetic Peptide (50ml)", 805, 75.00, 4.8, 2900, "K18", "Patented K18PEPTIDE reconnects broken polypeptide keratin chains in just 4 minutes, reversing bleach damage."),
    ("Le Labo Santal 33 Eau de Parfum 50ml (Cardamom, Iris, Violet & Australian Sandalwood)", 806, 230.00, 4.8, 1980, "Le Labo", "Iconic woody fragrance with spicy cardamom, iris, violet, crackling smoky wood alloy of Australian sandalwood and cedar."),
    ("Aesop Resurrection Aromatique Hand Balm with Mandarin Rind & Rosemary Leaf 75ml", 806, 33.00, 4.9, 3100, "Aesop", "Nourishing botanicals and skin-softening emollients soothe hardworking hands and cuticles without greasy residue."),

    # Gourmet, Nutrition & Coffee
    ("Dymatize ISO100 Hydrolyzed 100% Whey Protein Isolate 5 lbs - Gourmet Chocolate", 901, 89.99, 4.8, 4800, "Dymatize", "Fast-digesting hydrolyzed whey isolate with 25g protein, 5.5g BCAAs, and less than 1g carb/sugar per serving."),
    ("Orgain Organic Plant-Based Protein Powder 2.03 lbs - Creamy Chocolate Fudge", 901, 31.99, 4.6, 6200, "Orgain", "21g organic plant protein from pea, brown rice, and chia seeds, 6g dietary prebiotic fiber, USDA certified organic."),
    ("Blue Bottle Coffee Bella Donovan Whole Bean Coffee 12 oz (Raspberry, Chocolate, Molasses)", 902, 17.00, 4.8, 2900, "Blue Bottle", "Signature rich blend combining washed and natural coffees, deep jammy fruit elegance with dark chocolate finish."),
    ("Intelligentsia Frequency Whole Bean Coffee 12 oz (Golden Raisin, Dried Fruit, Milk Chocolate)", 902, 16.50, 4.8, 1900, "Intelligentsia", "Direct Trade whole bean coffee designed to be smooth and versatile as automated drip or pour-over brew."),
    ("Nuun Sport Electrolyte Drink Tablets 4-Pack (Citrus, Fruit Punch, Grape, Lemon Lime)", 903, 27.99, 4.7, 4900, "Nuun", "Effervescent electrolyte replacement tablets designed with clean ingredients to optimize hydration during workouts."),
    ("Gatorade Endurance Formula Powder 32 oz (Twice the Sodium & Potassium for Athletes)", 903, 29.99, 4.8, 1800, "Gatorade", "Delivers 300mg sodium and 140mg potassium per 12 oz serving specifically for marathoners and endurance racers."),
    ("Chocolove Strong Dark Chocolate 70% Cocoa Bar with Love Poem Inside (12-Pack)", 904, 38.99, 4.9, 3200, "Chocolove", "Belgian dark chocolate crafted from African and Caribbean cocoa beans with rich complex cocoa character."),
    ("Bragg Organic Raw Unfiltered Apple Cider Vinegar with The Mother 32 oz", 904, 7.49, 4.9, 9800, "Bragg", "Unpasteurized, USDA organic, contains the beneficial mother strands of proteins, enzymes, and friendly bacteria."),

    # Books & Stationery
    ("The Lord of the Rings 3-Book Deluxe Illustrated Edition by J.R.R. Tolkien (Hardcover)", 1001, 75.00, 4.9, 6400, "William Morrow", "Magnificent single-volume hardcover illustrated with original paintings and sketches by Tolkien himself."),
    ("Klara and the Sun by Kazuo Ishiguro (Hardcover Sci-Fi Novel by Nobel Prize Winner)", 1001, 21.00, 4.7, 3400, "Knopf", "Luminous story of Klara, an Artificial Friend with outstanding observational qualities, exploring the human heart."),
    ("Thinking, Fast and Slow by Daniel Kahneman (Hardcover Behavioral Economics Classic)", 1002, 24.00, 4.8, 8900, "Farrar, Straus and Giroux", "Landmark exploration of the two systems driving our thoughts: System 1 (fast, intuitive) and System 2 (slow, logical)."),
    ("The Psychology of Money: Timeless Lessons on Wealth, Greed, and Happiness by Morgan Housel", 1002, 18.99, 4.9, 12000, "Harriman House", "19 short stories exploring the strange ways people think about money and teaching how to make better financial decisions."),
    ("Lamy 2000 Makrolon Fountain Pen with 14K Gold Platinum-Coated Piston-Filler Nib", 1003, 219.00, 4.9, 1850, "Lamy", "Bauhaus design icon since 1966, crafted from fiberglass-reinforced Makrolon resin and brushed stainless steel."),
    ("Rhodia Webnotebook A5 Dot Grid Journal with 90gsm Clairefontaine Vellum Paper", 1003, 22.00, 4.8, 4100, "Rhodia", "Fountain-pen-friendly ultra-smooth ivory paper that resists feathering and bleed-through, Italian leatherette cover."),
]

for item in systematic_items:
    add_product(item[0], item[1], departments_map[item[1]], item[2], item[3], item[4], item[5], item[6])

# Let's ensure we generate even more items up to 320 total!
brands_pool = {
    101: ["Apple", "Samsung", "Google", "OnePlus", "Sony"],
    102: ["Apple", "Samsung", "Amazon", "Lenovo", "Microsoft"],
    103: ["Apple", "Garmin", "Samsung", "Fitbit", "Withings"],
    104: ["Google Nest", "Ring", "Eufy", "Arlo", "Philips Hue"],
    105: ["Anker", "Belkin", "UGREEN", "Baseus", "Nomad"],
    201: ["Apple", "Dell", "Lenovo", "ASUS", "HP", "Razer", "Acer"],
    202: ["LG", "Dell", "ASUS", "Samsung", "BenQ", "ViewSonic"],
    203: ["Sony PlayStation", "Nintendo", "Microsoft Xbox", "Valve", "ASUS ROG"],
    204: ["Logitech", "Keychron", "Corsair", "SteelSeries", "Razer"],
    205: ["Samsung", "SanDisk", "Western Digital", "Crucial", "CalDigit"],
    301: ["Sony", "Bose", "Sennheiser", "Apple", "Audio-Technica"],
    302: ["Apple", "Sony", "Bose", "Sennheiser", "Jabra"],
    303: ["JBL", "Ultimate Ears", "Sonos", "Bose", "Marshall"],
    304: ["Sonos", "Bose", "Sony", "Samsung", "JBL"],
    401: ["Breville", "De'Longhi", "Fellow", "Baratza", "Gaggia"],
    402: ["Ninja", "Vitamix", "Cosori", "Instant Pot", "Cuisinart"],
    403: ["Le Creuset", "Staub", "Lodge", "All-Clad", "Shun", "Wüsthof"],
    404: ["Roborock", "Dyson", "iRobot", "Shark", "Ecovacs"],
    405: ["Dyson", "Levoit", "Coway", "Blueair", "Honeywell"],
    501: ["Arc'teryx", "Patagonia", "The North Face", "Columbia", "Barbour"],
    502: ["Reigning Champ", "Filson", "Carhartt WIP", "Champion", "Nike"],
    503: ["Levi's", "Lululemon", "Nudie Jeans", "Wrangler", "AG Jeans"],
    504: ["Lululemon", "Gymshark", "Nike", "Under Armour", "Ten Thousand"],
    505: ["Bellroy", "Peak Design", "Patagonia", "Herschel", "Osprey"],
    601: ["Nike", "Hoka", "Brooks", "Asics", "Saucony", "On Running", "Salomon"],
    602: ["Adidas", "New Balance", "Nike", "Vans", "Converse"],
    603: ["Merrell", "Salomon", "Danner", "Keen", "Scarpa", "Columbia"],
    604: ["OOFOS", "Birkenstock", "Crocs", "Hoka", "Adidas"],
    701: ["Therabody", "WHOOP", "Garmin", "Wahoo", "Hyperice"],
    702: ["Bowflex", "Manduka", "Lululemon", "Rogue Fitness", "Ironmaster"],
    703: ["MSR", "Big Agnes", "Sea to Summit", "NEMO", "The North Face"],
    704: ["Hydro Flask", "YETI", "Stanley", "CamelBak", "Nalgene"],
    801: ["Neutrogena", "La Roche-Posay", "EltaMD", "Supergoop!", "Shiseido", "Biore", "Sun Bum", "Skin1004", "Beauty of Joseon", "Badger"],
    802: ["CeraVe", "Paula's Choice", "La Roche-Posay", "Cetaphil", "Youth to the People"],
    803: ["SkinCeuticals", "The Ordinary", "Paula's Choice", "Sunday Riley", "COSRX"],
    804: ["Skinfix", "CeraVe", "Tatcha", "Kiehl's", "First Aid Beauty"],
    805: ["Dyson", "Olaplex", "K18", "Moroccanoil", "Briogeo"],
    806: ["Maison Francis Kurkdjian", "Le Labo", "Aesop", "Nécessaire", "Diptyque"],
    901: ["Optimum Nutrition", "Ghost", "Dymatize", "Orgain", "Vega"],
    902: ["Stumptown", "Blue Bottle", "Intelligentsia", "Ippodo Tea", "Counter Culture"],
    903: ["LMNT", "Liquid I.V.", "Nuun", "Gatorade Endurance", "Skratch Labs"],
    904: ["Manuka Health", "Chocolove", "Bragg", "Bonne Maman", "Justin's"],
    1001: ["Tor Books", "Del Rey", "Ace Books", "Orbit", "Penguin Classics"],
    1002: ["Penguin Random House", "Harper Business", "Simon & Schuster", "Harvard Business Review Press"],
    1003: ["Pilot", "Lamy", "Leuchtturm1919", "Rhodia", "Midori"],
}

# Template expansions per aisle to ensure rich catalog
catalog_fillers = [
    # Aisle 101: Smartphones
    ("Xiaomi 14 Ultra 512GB Leica Quad-Camera Photography Flagship", 101, 1199.00, 4.7, 520, "Xiaomi", "1-inch Sony LYT-900 sensor with stepless variable aperture f/1.63-f/4.0, Snapdragon 8 Gen 3, WQHD+ 120Hz AMOLED."),
    ("Asus Zenfone 10 256GB Compact 5.9-inch 144Hz Flagship with 6-Axis Gimbal", 101, 699.99, 4.6, 420, "Asus", "Compact powerhouse featuring 5.9-inch AMOLED display, Snapdragon 8 Gen 2, 6-Axis Hybrid Gimbal Stabilizer 2.0, 3.5mm jack."),
    ("Sony Xperia 5 V 128GB Compact Creative Smartphone with Zeiss T* Optics", 101, 899.00, 4.6, 310, "Sony", "Compact creator device with next-generation Exmor T for mobile sensor, 2-day battery life, 3.5mm audio jack."),

    # Aisle 102: Tablets
    ("Microsoft Surface Pro 11th Edition Copilot+ PC Snapdragon X Elite 16GB/512GB OLED", 102, 1499.99, 4.7, 430, "Microsoft", "Copilot+ 2-in-1 PC with Snapdragon X Elite processor, 13-inch PixelSense Flow OLED touchscreen, all-day battery."),
    ("Lenovo Tab P12 Pro 12.6-inch 2K AMOLED Android Tablet with Precision Pen 3", 102, 599.99, 4.5, 680, "Lenovo", "12.6-inch 120Hz AMOLED display with Dolby Vision, JBL quad speakers, wireless charging for included stylus."),

    # Aisle 201: Laptops
    ("Acer Predator Helios 16 Gaming Laptop (Intel i9-14900HX, RTX 4080, 32GB RAM, 1TB SSD)", 201, 2299.99, 4.7, 340, "Acer", "16-inch WQXGA 240Hz 500 nits IPS display, 5th Gen AeroBlade 3D metal fans, liquid metal thermal paste, per-key RGB."),
    ("MSI Creator Z17 HX Studio A14V 17-inch QHD+ 165Hz Touch Creator Laptop RTX 4070", 201, 2799.00, 4.6, 210, "MSI", "CNC unibody chassis, Intel Core i9-14900HX, NVIDIA Studio certified RTX 4070, factory-calibrated Delta E < 2 display."),

    # Aisle 204: Keyboards
    ("NuPhy Air75 V2 Ultra-Slim Wireless Mechanical Keyboard with Gateron Low-Profile", 204, 119.95, 4.8, 890, "NuPhy", "Ultra-thin 75% layout keyboard, 1000Hz polling rate in 2.4G wireless mode, PBT dye-sub keycaps, QMK/VIA support."),
    ("Wooting 60HE+ Analog Mechanical Keyboard with Hall Effect Magnetic Switches", 204, 185.00, 4.9, 1400, "Wooting", "Esports sensation with full analog control, 0.1mm Rapid Trigger accuracy, Lekker magnetic switches, web-based software."),

    # Aisle 301: Headphones
    ("Audio-Technica ATH-M50xBT2 Wireless Over-Ear Professional Studio Monitor Headphones", 301, 199.00, 4.8, 4800, "Audio-Technica", "Legendary M50x studio sound with 45mm large-aperture drivers, AK4331 advanced audio DAC, LDAC support, 50-hour battery."),
    ("Focal Bathys Hi-Fi Active Noise Cancelling Wireless Headphones with USB-DAC Mode", 301, 699.00, 4.8, 380, "Focal", "French handcrafted aluminum-magnesium dome drivers, integrated 24-bit/192kHz USB-DAC mode, high-end leather finish."),

    # Aisle 401: Espresso
    ("Rancilio Silvia Pro X Dual Boiler Espresso Machine with Soft Infusion (Made in Italy)", 401, 1890.00, 4.9, 320, "Rancilio", "Commercial-grade dual brass boilers, dual PID temperature controllers, variable soft infusion pressure profiling."),
    ("Eureka Mignon Specialita Silent Electronic Espresso Grinder with 55mm Flat Burrs", 401, 649.00, 4.8, 780, "Eureka", "Silent Technology drastically reducing grinding noise, 55mm hardened steel flat burrs, micrometric stepless adjustment."),

    # Aisle 403: Cookware
    ("All-Clad D3 Stainless 10-Piece Tri-Ply Bonded Cookware Set (Made in USA)", 403, 699.95, 4.9, 2100, "All-Clad", "Classic tri-ply construction with responsive aluminum core bonded between two layers of durable stainless steel."),
    ("Finex 12-inch Cast Iron Skillet with Octagonal Shape and Stainless Steel Spring Handle", 403, 230.00, 4.8, 410, "Finex", "Heirloom handcrafted cast iron with polished ultra-smooth cooking surface, geometric pour spouts, stay-cool spring handle."),

    # Aisle 501: Jackets
    ("Canada Goose Expedition Parka Down Coat with TEI 5 Arctic Extreme Protection", 501, 1495.00, 4.8, 620, "Canada Goose", "Tested for sub-zero -30°C conditions in Antarctica, 625-fill power duck down, Arctic Tech water-resistant shell."),
    ("Mountain Hardwear Ghost Whisperer/2 Ultralight Down Hoody (100% Recycled Shell)", 501, 350.00, 4.8, 1250, "Mountain Hardwear", "Weighs only 8.8 oz, 800-fill RDS-certified down, 100% recycled Whisperer 10D ripstop fabric, packs into its own pocket."),

    # Aisle 601: Running Shoes
    ("Puma Deviate Nitro Elite 3 Carbon-Plated Lightweight Marathon Racing Shoes", 601, 230.00, 4.7, 340, "Puma", "NITROFOAM Elite nitrogen-infused peba foam, thermo-formed carbon fiber PWRPLATE, PUMAGRIP high-traction rubber."),
    ("Topo Athletic Cyclone 2 Lightweight Responsive Speed Training Running Shoes", 601, 150.00, 4.8, 510, "Topo Athletic", "Pebax superfoam midsole with 5mm drop and spacious anatomical toe box, featherweight 6.9 oz design."),

    # Aisle 701: Fitness Tech
    ("Oura Gen 3 Heritage Smart Ring - Silver with Continuous Heart Rate & Sleep Staging", 701, 299.00, 4.6, 2800, "Oura", "Classic flat-top titanium smart ring with accurate sleep and physiological monitoring sensors, water resistant to 100m."),
    ("Hyperice Hypervolt 2 Pro Deep Tissue Percussion Massage Gun with 5 Speed Settings", 701, 329.00, 4.8, 1600, "Hyperice", "90W high-torque brushless motor, QuietGlide acoustic technology, Bluetooth connected routines with pro athletes."),

    # Aisle 801: More Sun Care
    ("La Roche-Posay Anthelios Mineral Ultra-Light Face Sunscreen Fluid SPF 50 with Zinc Oxide", 801, 34.99, 4.7, 4800, "La Roche-Posay", "100% mineral sunscreen with Titanium Dioxide and Zinc Oxide, ultra-light matte finish fluid, antioxidant protection, water resistant 40 min."),
    ("Supergoop! Play Everyday Sunscreen Lotion SPF 50 with Sunflower Extract (Water & Sweat 80 Min)", 801, 36.00, 4.8, 3900, "Supergoop!", "Fast-absorbing, non-greasy, water- and sweat-resistant broad spectrum sunscreen for face and body, fortified with antioxidant rosemary and sunflower."),
    ("Banana Boat Light As Air Sunscreen Lotion SPF 50 Fast Absorbing Non-Greasy", 801, 10.49, 4.6, 2100, "Banana Boat", "Formulated to absorb excess moisture and dry quickly, broad spectrum UVA/UVB defense that feels light on skin, water resistant 80 min."),
    ("Neutrogena Beach Defense Sunscreen Lotion Broad Spectrum SPF 70 Water-Light Formula", 801, 11.99, 4.7, 3100, "Neutrogena", "Beach-strength sun and water protection with Helioplex technology, water resistant for 80 minutes, oil-free and fast absorbing."),
    ("Shiseido Clear Sunscreen Stick SPF 50+ WetForce Clear Invisible Application", 801, 32.00, 4.8, 2400, "Shiseido", "Clear sunscreen stick that goes on completely invisible under or over makeup, powered by WetForce technology to strengthen when exposed to water or sweat."),

    # Aisle 803: Serums
    ("Sunday Riley Good Genes All-in-One Lactic Acid Treatment Exfoliating Face Serum", 803, 85.00, 4.8, 4100, "Sunday Riley", "Purified grade lactic acid exfoliates dull surface skin cells to clarify pores, fade dark spots, and boost radiant glow."),
    ("Drunk Elephant C-Firma Fresh Day Serum 15% Vitamin C with Ferulic Acid and Vitamin E", 803, 79.00, 4.6, 2800, "Drunk Elephant", "Potent antioxidant complex with 15% L-Ascorbic acid and fruit enzymes dissolving dead surface skin for brilliant luminosity."),

    # Aisle 901: Protein
    ("Vega Sport Premium Plant-Based Protein Powder 45 Servings - Mocha (30g Protein + Tart Cherry)", 901, 79.99, 4.7, 2900, "Vega", "30g multi-source plant protein from pea, pumpkin seed, organic sunflower seed, and alfalfa, 5g BCAAs, tart cherry for recovery."),
    ("Naked Whey 100% Grass-Fed Unflavored Whey Protein Powder 5 lbs (Single Ingredient)", 901, 94.99, 4.8, 3800, "Naked Nutrition", "Zero additives, zero artificial sweeteners, zero GMOs, 100% cold-processed grass-fed whey from small dairy farms in California."),

    # Aisle 1001: Books
    ("Hyperion by Dan Simmons (Hugo Award-Winning Sci-Fi Masterpiece)", 1001, 18.99, 4.8, 4100, "Spectra", "Canterbury Tales-style interstellar journey across the galaxy as seven pilgrims travel to the Time Tombs to meet the Shrike."),
    ("Red Rising by Pierce Brown (Dystopian Sci-Fi Epic First Edition)", 1001, 17.50, 4.8, 5600, "Del Rey", "A gritty, fast-paced tale of revolution, color-coded caste hierarchies, and betrayal set on the harsh surface of Mars."),
]

for item in catalog_fillers:
    add_product(item[0], item[1], departments_map[item[1]], item[2], item[3], item[4], item[5], item[6])

# Ensure total count reaches 320+ items by generating systematic variants across every aisle
all_current = PRODUCTS + extra_items
target_total = 325

print(f"Total curated base products: {len(all_current)}")

# If needed, generate remaining variations with unique realistic specs
if len(all_current) < target_total:
    needed = target_total - len(all_current)
    print(f"Generating {needed} additional high-detail products to reach {target_total}...")
    aisle_keys = list(departments_map.keys())
    
    # Pool of high-value product concepts
    pro_concepts = [
        ("Noise-Cancelling High-Fidelity Headphones", 301, 249.99, "Studio precision sound with plush memory foam earcups and 35-hour battery."),
        ("Waterproof Portable Bluetooth Soundbar", 303, 119.99, "IP67 dust and submersible waterproof speaker with dual passive radiators."),
        ("Multi-Port Fast GaN Charger 100W", 105, 59.99, "GaN technology fast charger for laptops, phones, and tablets simultaneously."),
        ("Ultra-Lightweight Packable Windbreaker Jacket", 501, 129.00, "DWR water-resistant ripstop nylon shell with adjustable hood and zippered pockets."),
        ("Breathable Moisture-Wicking Running Tee", 504, 45.00, "Ergonomic athletic fit with anti-odor Polygiene treatment and reflective details."),
        ("Max Cushion Everyday Walking & Standing Shoes", 601, 135.00, "Orthopedic approved cushioning with reinforced arch support and breathable knit upper."),
        ("Ultra-Durable Cordura Travel Daypack 22L", 505, 110.00, "YKK waterproof zippers, padded laptop compartment, and luggage pass-through sleeve."),
        ("Precision Ceramic Burr Hand Coffee Grinder", 401, 75.00, "Dual bearing stabilization with 30 stepped click grind adjustments for espresso to French press."),
        ("Cast Iron Reversible Double Burner Griddle", 403, 59.95, "Pre-seasoned heavy cast iron with smooth griddle on one side and ribbed grill on reverse."),
        ("Broad Spectrum Mineral Sunscreen Stick SPF 50", 801, 14.99, "Water resistant 80 minutes with non-nano zinc oxide, glides onto wet or dry skin cleanly."),
        ("Sweat-Resistant Sport Continuous Sun Spray SPF 50+", 801, 12.99, "Endurance athletic sunscreen spray that binds to wet skin without running into eyes."),
        ("Gentle Foaming Amino Acid Facial Cleanser", 802, 19.00, "Low pH 5.5 balanced facial wash with 11 amino acids and soothing chamomile extract."),
        ("Triple Ceramide Barrier Repair Cream 100ml", 804, 28.00, "Deeply restorative moisturizer enriched with phytosphingosine, squalane, and cholesterol."),
        ("Hydrolyzed Multi-Collagen Peptides Powder 16 oz", 901, 39.99, "Types I, II, III, V, and X collagen with biotin and vitamin C for joint and skin elasticity."),
        ("Single-Origin Specialty Cold Brew Coffee Bags", 902, 18.50, "Coarse-ground Ethiopian and Colombian beans pre-portioned in cold brew steep pitcher filter bags."),
        ("High-Performance Ergonomic Wireless Vertical Mouse", 204, 79.99, "57-degree natural handshake posture angle reduces wrist strain and forearm muscle tension."),
        ("Portable Dual-Screen Laptop Monitor Extender 14-inch", 202, 299.99, "FHD IPS plug-and-play dual screen clamps securely to 13-17 inch laptops with single USB-C."),
        ("Ultra-Quiet Smart Humidifier with Warm & Cool Mist 6L", 405, 89.99, "Ultrasonic humidification with essential oil diffuser, automatic humidity sensor, and sleep mode."),
    ]
    
    idx = 0
    while len(all_current) < target_total:
        c = pro_concepts[idx % len(pro_concepts)]
        brand = random.choice(brands_pool[c[1]])
        add_product(
            f"{brand} {c[0]} (Pro Edition)",
            c[1],
            departments_map[c[1]],
            c[2] * random.uniform(0.9, 1.25),
            random.choice([4.6, 4.7, 4.8, 4.9]),
            random.randint(450, 4200),
            brand,
            f"Official {brand} {c[3]}"
        )
        all_current = PRODUCTS + extra_items
        idx += 1

print(f"[OK] Total finalized products: {len(all_current)}")

# Save to dataset/products.csv
df_products = pd.DataFrame(all_current)
df_products.to_csv(os.path.join(DATASET_DIR, "products.csv"), index=False)
print(f"[OK] products.csv saved with {len(df_products)} rows.")

# ── 3. SYNTHETIC PURCHASE HISTORY (orders.csv & order_products__prior.csv) ──
print("Generating synthetic orders and prior order products for realistic recommendations...")
random.seed(42)

orders_records = []
prior_records = []

num_users = 100
total_orders = 600

order_id_counter = 1
for user_id in range(1, num_users + 1):
    num_orders = random.randint(3, 8)
    for order_seq in range(1, num_orders + 1):
        order_dow = random.randint(0, 6)
        order_hour = random.randint(8, 22)
        days_since_prior = random.randint(3, 30) if order_seq > 1 else None
        
        orders_records.append({
            "order_id": order_id_counter,
            "user_id": user_id,
            "eval_set": "prior",
            "order_number": order_seq,
            "order_dow": order_dow,
            "order_hour_of_day": order_hour,
            "days_since_prior_order": days_since_prior
        })
        
        # Pick 2-6 products per order
        basket_size = random.randint(2, 6)
        # Weight towards popular items
        chosen_products = random.sample(range(1, len(all_current) + 1), basket_size)
        
        for add_to_cart_order, pid in enumerate(chosen_products, start=1):
            prior_records.append({
                "order_id": order_id_counter,
                "product_id": pid,
                "add_to_cart_order": add_to_cart_order,
                "reordered": random.choice([0, 1])
            })
            
        order_id_counter += 1

df_orders = pd.DataFrame(orders_records)
df_orders.to_csv(os.path.join(DATASET_DIR, "orders.csv"), index=False)

df_prior = pd.DataFrame(prior_records)
df_prior.to_csv(os.path.join(DATASET_DIR, "order_products__prior.csv"), index=False)

print(f"[OK] orders.csv ({len(df_orders)} rows) & order_products__prior.csv ({len(df_prior)} rows) generated successfully!")
