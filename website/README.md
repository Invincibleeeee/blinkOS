# 👁️ Blink OS - Website

![Blink OS](https://img.shields.io/badge/Blink%20OS-Production%20Ready-success)
![React](https://img.shields.io/badge/React-19.1.1-blue)
![Vite](https://img.shields.io/badge/Vite-7.1.9-purple)
![License](https://img.shields.io/badge/License-MIT-green)

The official website for **Blink OS** - a revolutionary hands-free computer control system using iris and head tracking technology. Built with React, Vite, and Tailwind CSS for a premium, minimalist user experience.

## 🌟 Features

- **Minimalist Design** - Apple-inspired black/white/gray aesthetic
- **Blazing Fast** - Optimized hover effects (100ms transitions)
- **Fully Responsive** - Mobile-first design with adaptive layouts
- **Interactive Demos** - Video demonstrations with full controls
- **Active Navigation** - Real-time navbar highlighting
- **Smooth Animations** - Framer Motion powered transitions
- **GPU Accelerated** - Hardware-accelerated transforms for 60fps performance

## 🚀 Live Demo

Visit the live website: [Your Deployment URL]

GitHub Repository: [https://github.com/Invincibleeeee/blinkOS](https://github.com/Invincibleeeee/blinkOS)

## 📋 Pages

1. **Home** - Hero section with feature highlights and CTA buttons
2. **Mission** - Project vision, values, and impact statistics
3. **How It Works** - Technical explanation with EAR formula
4. **Demo** - Interactive demos with iris & head tracking videos
5. **Applications** - Use cases and comparison with traditional solutions

## 🛠️ Tech Stack

### Frontend Framework
- **React 19.1.1** - Latest React with concurrent features
- **Vite 7.1.9** - Next-generation build tool with HMR

### Styling & Animation
- **Tailwind CSS 4.1.14** - Utility-first CSS framework
- **Framer Motion 12.23.22** - Production-ready animation library
- **Lucide React 0.544.0** - Beautiful open-source icons

### Routing
- **Custom Router** - Lightweight history API-based routing

### Core Technologies (Backend)
- **OpenCV-Python** - Computer vision library
- **MediaPipe** - ML solutions for live perception
- **NumPy** - Numerical computing
- **PyAutoGUI** - GUI automation
- **SciPy** - Scientific computing

## 📦 Installation

### Prerequisites
- Node.js 18+ and npm/yarn/pnpm
- Git

### Clone Repository
```bash
git clone https://github.com/Invincibleeeee/blinkOS.git
cd blinkOS/frontend
```

### Install Dependencies
```bash
npm install
# or
yarn install
# or
pnpm install
```

### Start Development Server
```bash
npm run dev
```

Visit `http://localhost:5173` in your browser.

## 🏗️ Build for Production

```bash
npm run build
```

The optimized build will be created in the `dist/` directory.

### Preview Production Build
```bash
npm run preview
```

## 📁 Project Structure

```
frontend/
├── public/              # Static assets
│   └── vite.svg
├── src/
│   ├── assets/          # Images and media
│   │   └── react.svg
│   ├── components/      # Reusable components
│   │   ├── Footer.jsx   # Footer with social links
│   │   ├── Navbar.jsx   # Navigation with active highlighting
│   │   └── Router.jsx   # Custom routing system
│   ├── pages/           # Page components
│   │   ├── Home.jsx     # Landing page
│   │   ├── Mission.jsx  # Mission & values
│   │   ├── HowItWorks.jsx  # Technical details
│   │   ├── Demo.jsx     # Interactive demos
│   │   └── Applications.jsx # Use cases
│   ├── App.jsx          # Main app component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles & animations
├── eye.mp4              # Iris tracking demo video
├── head.mp4             # Head tracking demo video
├── index.html           # HTML template
├── package.json         # Dependencies
├── vite.config.js       # Vite configuration
├── vercel.json          # Vercel deployment config
└── README.md            # This file
```

## 🎨 Design System

### Colors
- **Background**: Pure Black (#000000)
- **Text Primary**: White (#FFFFFF)
- **Text Secondary**: Neutral 400 (#A3A3A3)
- **Text Tertiary**: Neutral 500 (#737373)
- **Borders**: White/10 (rgba(255,255,255,0.1))

### Typography
- **Font Family**: -apple-system, SF Pro Display, Segoe UI
- **Heading Sizes**: 4xl/5xl/6xl
- **Body Text**: xs/sm

### Animations
- **Page Load**: 0.3s fadeInUp
- **Hover Effects**: 0.1s with GPU acceleration
- **Transitions**: cubic-bezier(0.4, 0, 0.2, 1)

## 🚢 Deployment

### Deploy to Vercel (Recommended)

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Follow the prompts and your site will be live!

### Alternative Platforms
- **Netlify**: Drag & drop `dist/` folder
- **GitHub Pages**: Use `gh-pages` branch
- **Railway**: Connect GitHub repo

## ⚡ Performance Optimizations

- **Code Splitting**: Automatic route-based splitting
- **Lazy Loading**: Dynamic imports for heavy components
- **Image Optimization**: WebP format with fallbacks
- **Font Loading**: System fonts for instant rendering
- **CSS Purging**: Unused styles removed in production
- **Tree Shaking**: Dead code elimination
- **Minification**: JS, CSS, and HTML compression
- **GPU Acceleration**: Hardware-accelerated transforms

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root:
```env
VITE_API_URL=your_api_url
VITE_ANALYTICS_ID=your_analytics_id
```

### Vite Config
Customize `vite.config.js` for build settings, plugins, and server options.

## 📝 Scripts

```json
{
  "dev": "vite",              // Start dev server
  "build": "vite build",      // Production build
  "preview": "vite preview",  // Preview production build
  "lint": "eslint ."          // Run ESLint
}
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [React](https://react.dev/) - UI library
- [Vite](https://vite.dev/) - Build tool
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
- [Framer Motion](https://www.framer.com/motion/) - Animation library
- [Lucide Icons](https://lucide.dev/) - Icon set

## 📧 Contact

- **GitHub**: [@Invincibleeeee](https://github.com/Invincibleeeee)
- **Project**: [Blink OS](https://github.com/Invincibleeeee/blinkOS)

## 🌟 Show Your Support

If you like this project, please give it a ⭐ on GitHub!

---

**Made with ❤️ for accessibility**
