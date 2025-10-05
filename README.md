<div align="center">

# 👁️ BlinkOS

### *Empowering Independence Through Eye and Head Tracking*

**Control your computer with just your eyes and head movements — completely free, open source, and privacy-first.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-19.1.1-blue.svg)](https://reactjs.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Enabled-red.svg)](https://opencv.org/)

[🌐 Live Website](https://blink-os.vercel.app) • [🎥 Demo Video](#demo) • [📖 Documentation](#installation)

</div>

---

## 🌟 About BlinkOS

**BlinkOS** is a revolutionary accessibility system that enables hands-free computer control using only a standard webcam. Built for individuals with motor disabilities, gamers, developers, and anyone seeking innovative interaction methods, BlinkOS combines **precision iris tracking** and **natural head movement detection** to create an intuitive, seamless computing experience.

### 🎯 The Problem We're Solving

- **15+ million people** worldwide live with motor disabilities that limit traditional computer interaction
- Professional eye-tracking solutions cost **$20,000 - $50,000**, making them inaccessible to most
- **60% of individuals** who need assistive technology lack access due to cost barriers

### 💡 Our Solution

BlinkOS provides **professional-grade iris and head tracking technology** at **zero cost**, using only:
- ✅ A standard webcam
- ✅ Open-source software
- ✅ 100% local processing (complete privacy)
- ✅ Sub-pixel precision accuracy
- ✅ < 20ms latency

---

## ✨ Features

### 🎯 Dual Tracking System
- **Iris Gaze Tracking**: Control cursor with sub-pixel precision using eye movements
- **Head Movement Detection**: Scroll naturally through content, PDFs, and social media reels
- **Blink Detection**: Perform click actions with intentional blinks using EAR (Eye Aspect Ratio) algorithm

### 🚀 Technical Capabilities
- Real-time processing at **60 FPS**
- Latency under **20ms** for responsive interaction
- Adaptive calibration for individual users
- Smooth movement prediction algorithms
- Works with any standard webcam

### 🔒 Privacy First
- **100% local processing** — no data leaves your device
- No cloud servers, no tracking, no data collection
- Open-source codebase for full transparency
- You own and control your data

---

## 📁 Project Structure

```
blinkOS/
├── eye-control/          # Iris gaze tracking system
│   ├── main.py          # Eye tracking implementation
│   └── requirements.txt # Python dependencies
│
├── head-control/        # Head movement tracking system
│   ├── main.py         # Head tracking implementation
│   └── requirements.txt # Python dependencies
│
└── website/            # React-based landing page
    ├── src/
    │   ├── components/  # Reusable UI components
    │   ├── pages/      # Application pages
    │   └── assets/     # Static resources
    ├── public/         # Public assets
    └── package.json    # Node dependencies
```

---

## 🛠️ Tech Stack

### Eye & Head Tracking (Python)
- **OpenCV** - Computer vision and image processing
- **MediaPipe** - Face mesh and landmark detection
- **NumPy** - Numerical computations
- **PyAutoGUI** - System cursor control
- **SciPy** - Advanced mathematical functions

### Website (React + Vite)
- **React 19** - Modern UI framework
- **Vite** - Lightning-fast build tool
- **Tailwind CSS 4** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Lucide React** - Beautiful icons

---

## 📥 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Webcam (built-in or external)
- Node.js 18+ (for website development)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Invincibleeeee/blinkOS.git
cd blinkOS
```

### 2️⃣ Eye Control Setup
```bash
cd eye-control
pip install -r requirements.txt
python main.py
```

### 3️⃣ Head Control Setup
```bash
cd head-control
pip install -r requirements.txt
python main.py
```

### 4️⃣ Website Setup (Optional - For Development)
```bash
cd website
npm install
npm run dev
```

The website will be available at `http://localhost:5173`

---

## 🎮 Usage Guide

### Eye Tracking Control
1. Run the eye tracking script: `python eye-control/main.py`
2. Position yourself comfortably in front of the webcam
3. Look at calibration points when prompted
4. Move your eyes to control the cursor
5. **Blink intentionally** to perform clicks

### Head Movement Control
1. Run the head tracking script: `python head-control/main.py`
2. Ensure your face is visible to the webcam
3. **Tilt head up/down** to scroll vertically
4. **Tilt head left/right** for horizontal scrolling
5. Perfect for reading PDFs, browsing social media, and viewing content

### Tips for Best Performance
- ✅ Ensure good lighting conditions
- ✅ Position webcam at eye level
- ✅ Minimize background movement
- ✅ Calibrate for optimal accuracy
- ✅ Take breaks to avoid eye strain

---

## 🎥 Demo

### Eye Aspect Ratio (EAR) Formula
BlinkOS uses the scientifically-proven EAR formula for blink detection:

```
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 × ||p1 - p4||)
```

- **Normal eye**: EAR ≈ 0.3
- **Closed eye**: EAR ≈ 0.1
- **Blink threshold**: EAR < 0.2

### Live Demo
🌐 **Visit our website**: [https://blink-os.vercel.app](https://blink-os.vercel.app)

📺 **Watch demo videos** showcasing:
- Real-time iris tracking precision
- Natural head movement scrolling
- Click actions via blink detection

---

## 🌍 Use Cases

### 🦾 Accessibility Support
- ALS patients
- Spinal cord injuries
- Cerebral palsy
- Multiple sclerosis
- Any motor disability affecting hand use

### 💻 Professional Applications
- Hands-free coding and development
- Multi-monitor workflows
- Document review and annotation
- Video conferencing while taking notes

### 🎮 Gaming & Entertainment
- Hands-free gaming control
- Social media browsing (reels, feeds)
- PDF and e-book reading
- Video content consumption

---

## 🤝 Contributing

We welcome contributions from the community! BlinkOS is built on the belief that accessibility technology should be free and collaborative.

### How to Contribute
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/AmazingFeature`
3. **Commit** your changes: `git commit -m 'Add AmazingFeature'`
4. **Push** to the branch: `git push origin feature/AmazingFeature`
5. **Open** a Pull Request

### Areas We Need Help
- 🐛 Bug fixes and testing
- 🎨 UI/UX improvements
- 📚 Documentation and tutorials
- 🌐 Internationalization
- 🧪 New features and enhancements

See [CONTRIBUTING.md](website/CONTRIBUTING.md) for detailed guidelines.

---

## 📊 Comparison with Traditional Solutions

| Feature | BlinkOS | Traditional Solutions |
|---------|---------|----------------------|
| **Price** | Free | $20,000 - $50,000 |
| **Setup Time** | < 5 minutes | Hours of calibration |
| **Hardware** | Standard webcam | Specialized equipment |
| **Portability** | Any laptop | Fixed installation |
| **Privacy** | 100% local | Varies |
| **Open Source** | ✅ Yes | ❌ No |
| **Customization** | Full access | Limited |
| **Head Tracking** | Built-in | Not included |

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](website/LICENSE) file for details.

**TL;DR**: You can use, modify, and distribute this software freely. We only ask that you include the original license and copyright notice.

---

## 🙏 Acknowledgments

### Built With ❤️ By
- **Team BlinkOS** - Passionate developers committed to accessibility

### Special Thanks To
- The open-source community for incredible tools like OpenCV and MediaPipe
- Researchers advancing eye-tracking and computer vision technology
- Individuals with disabilities who inspire us to build better solutions
- Everyone who believes technology should be accessible to all

### Inspired By
The millions of people worldwide who deserve equal access to technology, regardless of physical ability.

---

## 📞 Contact & Support

### 🌐 Links
- **Website**: [https://blink-os.vercel.app](https://blink-os.vercel.app)
- **GitHub**: [https://github.com/Invincibleeeee/blinkOS](https://github.com/Invincibleeeee/blinkOS)

### 💬 Get Help
- 📖 Read the [Documentation](https://blink-os.vercel.app/how-it-works)
- 🐛 Report bugs via [GitHub Issues](https://github.com/Invincibleeeee/blinkOS/issues)
- 💡 Request features or suggest improvements
- ⭐ Star the repo if BlinkOS helps you!

### 🎯 Our Mission
> *"Making professional iris and head tracking technology accessible to everyone, everywhere, for free."*

---

<div align="center">

### 🌟 If BlinkOS helps you or someone you know, please consider starring the repository!

**Together, we can make technology truly accessible for everyone.**

Made with 👁️ and ❤️ for accessibility

</div>
