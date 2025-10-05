import { motion } from 'framer-motion';
import { Accessibility, Gamepad, Code, BookOpen, Film, Smartphone, Check, X } from 'lucide-react';

export default function Applications() {
  const applications = [
    {
      icon: Accessibility,
      title: "Accessibility Support",
      description: "Enable individuals with motor disabilities to control computers using only their eyes and head movements",
      useCases: ["ALS patients", "Spinal cord injuries", "Cerebral palsy", "Multiple sclerosis"]
    },
    {
      icon: Gamepad,
      title: "Gaming Control",
      description: "Hands-free gaming experience with iris-based aiming and head tracking for camera control",
      useCases: ["First-person shooters", "Strategy games", "Adventure games", "Simulation"]
    },
    {
      icon: Code,
      title: "Developer Tools",
      description: "Code hands-free with iris-based cursor control and head tracking for scrolling through documentation",
      useCases: ["Code editing", "Debugging", "Documentation reading", "Terminal control"]
    },
    {
      icon: BookOpen,
      title: "Reading & Research",
      description: "Navigate PDFs and documents naturally with head tracking for smooth scrolling and iris precision for selection",
      useCases: ["PDF navigation", "Academic research", "E-book reading", "Document annotation"]
    },
    {
      icon: Film,
      title: "Content Consumption",
      description: "Scroll through social media reels and videos using natural head movements combined with iris focus",
      useCases: ["Social media browsing", "Video platforms", "News feeds", "Image galleries"]
    },
    {
      icon: Smartphone,
      title: "Productivity",
      description: "Enhance workflow with hands-free navigation, perfect for multitasking and reference work",
      useCases: ["Email management", "Calendar control", "Note-taking", "Video calls"]
    }
  ];

  const comparison = [
    { feature: "Price", blinkos: "Free", traditional: "$20,000 - $50,000" },
    { feature: "Setup Time", blinkos: "< 5 minutes", traditional: "Hours of calibration" },
    { feature: "Hardware", blinkos: "Standard webcam", traditional: "Specialized equipment" },
    { feature: "Portability", blinkos: "Any laptop", traditional: "Fixed installation" },
    { feature: "Accuracy", blinkos: "Sub-pixel precision", traditional: "High precision" },
    { feature: "Head Tracking", blinkos: "Built-in for scrolling", traditional: "Not included" },
    { feature: "Latency", blinkos: "< 20ms", traditional: "< 15ms" },
    { feature: "Open Source", blinkos: true, traditional: false },
    { feature: "Privacy", blinkos: "100% local", traditional: "Varies" },
    { feature: "Customization", blinkos: "Full access", traditional: "Limited" }
  ];

  return (
    <div className="min-h-screen bg-black text-white pt-24 pb-16">
      <div className="max-w-6xl mx-auto px-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="text-center mb-16"
        >
          <h1 className="text-4xl md:text-5xl font-semibold mb-4">
            Applications
          </h1>
          <p className="text-sm text-neutral-400 max-w-2xl mx-auto">
            Blink OS opens new possibilities for hands-free interaction across every digital experience
          </p>
        </motion.div>

        {/* Application Cards */}
        <div className="grid md:grid-cols-2 gap-4 mb-16">
          {applications.map((app, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.03 }}
              whileHover={{ y: -2, scale: 1.01, transition: { duration: 0.1, ease: 'easeOut' } }}
              className="bg-neutral-900/50 border border-white/10 rounded-2xl p-6 hover:border-white/20 transition-all duration-100"
            >
              <app.icon className="w-5 h-5 text-white mb-3" />
              <h3 className="text-base font-medium mb-2">{app.title}</h3>
              <p className="text-xs text-neutral-400 leading-relaxed mb-4">
                {app.description}
              </p>
              <div className="flex flex-wrap gap-2">
                {app.useCases.map((useCase, i) => (
                  <span
                    key={i}
                    className="text-xs px-3 py-1 bg-white/5 rounded-lg text-neutral-400"
                  >
                    {useCase}
                  </span>
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Comparison Table */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.3 }}
          className="mb-16"
        >
          <h2 className="text-xl font-medium mb-8 text-center">Blink OS vs Traditional Solutions</h2>
          <div className="bg-neutral-900/50 border border-white/10 rounded-2xl overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-white/10">
                    <th className="text-left text-xs font-medium text-neutral-400 px-6 py-4">Feature</th>
                    <th className="text-left text-xs font-medium px-6 py-4">Blink OS</th>
                    <th className="text-left text-xs font-medium text-neutral-400 px-6 py-4">Traditional</th>
                  </tr>
                </thead>
                <tbody>
                  {comparison.map((row, index) => (
                    <tr key={index} className="border-b border-white/5 last:border-0 hover:bg-white/5 transition-colors duration-200">
                      <td className="text-xs text-neutral-400 px-6 py-4">{row.feature}</td>
                      <td className="text-xs px-6 py-4">
                        {typeof row.blinkos === 'boolean' ? (
                          row.blinkos ? (
                            <Check className="w-4 h-4 text-white" />
                          ) : (
                            <X className="w-4 h-4 text-neutral-600" />
                          )
                        ) : (
                          <span className="font-medium">{row.blinkos}</span>
                        )}
                      </td>
                      <td className="text-xs text-neutral-400 px-6 py-4">
                        {typeof row.traditional === 'boolean' ? (
                          row.traditional ? (
                            <Check className="w-4 h-4 text-neutral-400" />
                          ) : (
                            <X className="w-4 h-4 text-neutral-600" />
                          )
                        ) : (
                          row.traditional
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </motion.div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.4 }}
          className="bg-neutral-900/50 border border-white/10 rounded-2xl p-8 text-center hover:border-white/20 transition-colors duration-200"
        >
          <h2 className="text-xl font-medium mb-3">Transform Your Digital Experience</h2>
          <p className="text-sm text-neutral-400 max-w-2xl mx-auto mb-6 leading-relaxed">
            Whether you need accessibility support or want to explore cutting-edge interaction methods, Blink OS delivers professional iris and head tracking at zero cost. Scroll reels & PDFs naturally with head movements, control cursors with iris precision.
          </p>
          <button className="px-6 py-2.5 bg-white text-black text-sm font-medium rounded-xl hover:bg-neutral-200 transition-colors duration-200">
            Start Using Blink OS
          </button>
        </motion.div>
      </div>
    </div>
  );
}
