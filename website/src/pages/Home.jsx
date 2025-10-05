import { motion } from 'framer-motion';
import { Eye, Zap, Shield, Sparkles } from 'lucide-react';
import { Link } from '../components/Router';

export default function Home() {
  const features = [
    {
      icon: Eye,
      title: "Precision Iris Tracking",
      description: "Advanced iris detection with sub-pixel accuracy for perfect cursor control"
    },
    {
      icon: Zap,
      title: "Head Movement Detection",
      description: "Natural head tracking for scrolling reels and reading PDFs effortlessly"
    },
    {
      icon: Shield,
      title: "100% Private",
      description: "All processing happens locally on your device. Zero data collection"
    },
    {
      icon: Sparkles,
      title: "Open Source & Free",
      description: "Completely free forever. No subscriptions, no hidden costs"
    }
  ];

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="flex items-center justify-center gap-3 mb-6"
          >
            <Eye className="w-6 h-6 text-white" />
            <span className="text-lg font-medium">Blink OS</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.1 }}
            className="text-4xl md:text-6xl font-semibold mb-6 leading-tight"
          >
            Control your computer
            <br />
            with just your eyes
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.2 }}
            className="text-sm text-neutral-400 mb-8 max-w-2xl mx-auto leading-relaxed"
          >
            Professional-grade iris and head tracking technology, completely free and open source.
            Navigate, click, and interact hands-free with precision iris control.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.3 }}
            className="flex flex-wrap gap-3 justify-center"
          >
            <Link to="/demo">
              <button className="px-6 py-2.5 bg-white text-black text-sm font-medium rounded-xl hover:bg-neutral-200 transition-colors">
                Get Started
              </button>
            </Link>
            <Link to="/demo">
              <button className="px-6 py-2.5 bg-white/5 text-white text-sm font-medium rounded-xl hover:bg-white/10 transition-colors border border-white/10">
                Watch Demo
              </button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-4">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.4 + index * 0.03 }}
                whileHover={{ 
                  y: -2, 
                  scale: 1.01,
                  transition: { duration: 0.1, ease: 'easeOut' }
                }}
                className="bg-neutral-900/50 border border-white/10 rounded-2xl p-6 hover:border-white/20 transition-all duration-100"
              >
                <feature.icon className="w-5 h-5 text-white mb-3" />
                <h3 className="text-base font-medium mb-2">{feature.title}</h3>
                <p className="text-xs text-neutral-400 leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.6 }}
            className="bg-neutral-900/50 border border-white/10 rounded-2xl p-8 hover:border-white/20 transition-colors duration-100"
          >
            <h2 className="text-xl font-medium mb-8 text-center">Why It Matters</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="text-2xl font-semibold mb-1">15M+</div>
                <div className="text-xs text-neutral-400">People with motor disabilities</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-semibold mb-1">$50K</div>
                <div className="text-xs text-neutral-400">Average cost of alternatives</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-semibold mb-1">$0</div>
                <div className="text-xs text-neutral-400">Blink OS - Forever free</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-semibold mb-1">100%</div>
                <div className="text-xs text-neutral-400">Open source</div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
