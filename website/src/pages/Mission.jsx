import { motion } from 'framer-motion';
import { Heart, Target, Zap, Users, Lightbulb, TrendingUp } from 'lucide-react';

export default function Mission() {
  const values = [
    {
      icon: Heart,
      title: "Accessibility First",
      description: "Making technology universally accessible through iris tracking"
    },
    {
      icon: Lightbulb,
      title: "Innovation",
      description: "Pioneering advanced head tracking for seamless interaction"
    },
    {
      icon: Users,
      title: "Empowerment",
      description: "Enabling independence for individuals with motor disabilities"
    },
    {
      icon: TrendingUp,
      title: "Progress",
      description: "Continuously advancing iris precision and head tracking capabilities"
    }
  ];

  const stats = [
    { value: "15M+", label: "People with motor disabilities worldwide" },
    { value: "60%", label: "Lack access to assistive technology" },
    { value: "$50K", label: "Average cost of existing iris tracking solutions" },
    { value: "$0", label: "Blink OS - Free and open source" }
  ];

  return (
    <div className="min-h-screen bg-black text-white pt-24 pb-16">
      <div className="max-w-6xl mx-auto px-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="text-center mb-16"
        >
          <h1 className="text-4xl md:text-5xl font-semibold mb-4">
            Our Mission
          </h1>
          <p className="text-sm text-neutral-400 max-w-2xl mx-auto">
            Democratizing iris and head tracking technology to create an inclusive digital world
          </p>
        </motion.div>

        {/* Personal Mission */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="mb-16 bg-neutral-900/50 border border-white/10 rounded-2xl p-8 hover:border-white/20 transition-colors"
        >
          <div className="flex items-start gap-4 mb-4">
            <Target className="w-5 h-5 text-white mt-1 flex-shrink-0" />
            <div>
              <h2 className="text-xl font-medium mb-3">Why Blink OS Exists</h2>
              <p className="text-sm text-neutral-400 leading-relaxed mb-3">
                Current iris tracking solutions cost tens of thousands of dollars, making them inaccessible to most people who need them. This creates a massive barrier for individuals with motor disabilities who could benefit from hands-free computer control.
              </p>
              <p className="text-sm text-neutral-400 leading-relaxed">
                Blink OS changes this. By combining precise iris tracking with advanced head tracking technology, we're providing a free, open-source solution that anyone can use to navigate computers, scroll through reels, read PDFs, and interact with digital content naturally.
              </p>
            </div>
          </div>
        </motion.div>

        {/* Values Grid */}
        <div className="grid md:grid-cols-2 gap-4 mb-16">
          {values.map((value, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.2 + index * 0.03 }}
              whileHover={{ y: -2, scale: 1.01, transition: { duration: 0.1, ease: 'easeOut' } }}
              className="bg-neutral-900/50 border border-white/10 rounded-2xl p-6 hover:border-white/20 transition-all duration-100"
            >
              <value.icon className="w-5 h-5 text-white mb-3" />
              <h3 className="text-base font-medium mb-2">{value.title}</h3>
              <p className="text-xs text-neutral-400 leading-relaxed">
                {value.description}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Market Reality */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.4 }}
          className="bg-neutral-900/50 border border-white/10 rounded-2xl p-8 hover:border-white/20 transition-colors"
        >
          <div className="flex items-start gap-4 mb-6">
            <Zap className="w-5 h-5 text-white mt-1 flex-shrink-0" />
            <h2 className="text-xl font-medium">The Reality</h2>
          </div>
          
          <div className="grid md:grid-cols-4 gap-6">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-2xl font-semibold mb-1">{stat.value}</div>
                <div className="text-xs text-neutral-400">{stat.label}</div>
              </div>
            ))}
          </div>

          <p className="text-sm text-neutral-400 leading-relaxed mt-6 pt-6 border-t border-white/10">
            Blink OS bridges this gap by providing professional-grade iris and head tracking technology at zero cost. Our open-source approach ensures continuous improvement and accessibility for everyone who needs it.
          </p>
        </motion.div>
      </div>
    </div>
  );
}
