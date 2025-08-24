

# 🚀 API Monitor Dashboard

A sophisticated API monitoring dashboard with world-class **3D animations** and **visual effects**.
Monitor your API endpoints in style with **real-time status tracking**, **response time monitoring**, and an immersive **3D UI**.

---

## ✨ Features

### Core Functionality

* **Real-time API Monitoring** – Track health & performance of your endpoints
* **Response Time Tracking** – Measure response speed with detailed metrics
* **Status Code Monitoring** – Visual indicators for success/failure
* **HTTP Method Support** – GET, POST, PUT, DELETE, PATCH
* **Endpoint Management** – Easily add and manage endpoints
* **Detailed Analytics** – Comprehensive endpoint detail pages

### Enhanced Visual Experience

* **3D Particle Systems** – Multi-layered starfield + floating shapes
* **Interactive Backgrounds** – Mouse-responsive parallax effects
* **Glass Morphism UI** – Modern frosted glass with backdrop blur
* **Smooth Animations** – 60fps transitions & entrance effects
* **3D Hover Effects** – Perspective-based interactivity
* **Gradient Text Effects** – Glowing & shimmering text animations

---

## 🎨 Visual Enhancements

The dashboard delivers a cinematic, modern look with:

* **Advanced 3D Backgrounds** featuring wireframe geometry
* **Immersive Mouse Tracking** for camera-style movement
* **Fluid Animation Library** for smooth UI transitions
* **Glass Morphism Design** across interface layers
* **Dynamic Gradient Overlays** for color depth
* **Responsive 3D Effects** adapting to user interaction

---

## 🚀 Getting Started

### Prerequisites

* A web server (Apache, Nginx, or Python’s built-in)
* Modern browser with **WebGL support**
* **Flask** (for backend functionality)

### Installation

1. **Clone or download** project files
2. **Serve HTML files** via your web server
3. **Configure Flask backend** for template rendering
4. **Open the dashboard** in your browser

### Quick Start (Python)

```bash
# Serve locally
python -m http.server 8000  

# Open in browser
open http://localhost:8000/dashboard.html  
```

---

## 🎯 Usage

### Adding Endpoints

1. Go to **Add Endpoint**
2. Enter details:

   * **Name** → A descriptive label
   * **URL** → The endpoint to monitor
   * **HTTP Method** → GET, POST, PUT, DELETE, PATCH
   * **Expected Status** → e.g., `200`
3. Save → Start monitoring instantly

### Dashboard View

* **Status Colors** → 🟢 success | 🔴 failure | ⚪ untested
* **Response Times** → Real-time performance graphs
* **Method Tags** → Color-coded for clarity
* **Interactive Clicks** → Drill into endpoint details

### Endpoint Details

* Response history
* Performance trends
* Status tracking
* Error logs & analysis

---

## 🎨 Customization

### Animation Settings

```js
// Particle system configuration
const particleCount   = 200;     // Background particle count
const animationSpeed  = 0.001;   // Speed multiplier
const mouseInfluence  = 0.0002;  // Mouse sensitivity
```

### Visual Themes

```css
:root {
  --primary-color: #3b82f6;
  --background-gradient: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  --glass-opacity: 0.1;
}
```

---

## 🌟 Browser Compatibility

* **Chrome/Edge** → Full support, best performance
* **Firefox** → Full support
* **Safari** → Supported (WebGL required)
* **Mobile** → Responsive, with optimized animations

---

## 🔧 Technical Details

### Performance Optimizations

* **requestAnimationFrame** → Smooth 60fps rendering
* **GPU Acceleration** → Hardware-boosted transforms
* **Optimized Particles** → Efficient rendering pipeline
* **Adaptive Design** → Works across screens

### Dependencies

* **No external libraries** – Pure HTML/CSS/JS
* **WebGL** for 3D rendering
* **Modern CSS** → backdrop-filter, transforms, animations

---

## 📱 Responsive Design

* **Desktop** → Full animations & effects
* **Tablet** → Optimized for touch
* **Mobile** → Lightweight animations

---

## 🤝 Contributing

Contributions are welcome! 🎉
Enhance visual effects, add animations, or extend monitoring features.

---

**Built with ❤️ and powered by world-class 3D animations.**


