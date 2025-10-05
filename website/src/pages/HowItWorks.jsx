import { motion } from 'framer-motion';
import { Camera, Eye, Cpu, MonitorPlay, Zap } from 'lucide-react';

export default function HowItWorks() {
  const steps = [
    {
      icon: Camera,
      title: "Camera Activation",
      description: "Blink OS accesses your webcam to capture real-time video feed for iris and head tracking analysis"
    },
    {
      icon: Eye,
      title: "Iris Detection",
      description: "Advanced computer vision algorithms identify and isolate your iris in each frame with high precision"
    },
    {
      icon: Cpu,
      title: "Movement Analysis",
      description: "Machine learning models analyze iris movement patterns and head position in real-time"
    },
    {
      icon: MonitorPlay,
      title: "Screen Mapping",
      description: "Iris position is mapped to screen coordinates, enabling precise cursor control and interaction"
    },
    {
      icon: Zap,
      title: "Iris & Head Prediction",
      description: "Predictive algorithms smooth movements and integrate head tracking for scrolling reels and reading PDFs naturally"
    }
  ];

  const features = [
    {
      title: "Dual Tracking System",
      points: [
        "Iris tracking for precise cursor control",
        "Head tracking for natural scrolling",
        "Combined prediction algorithms",
        "Sub-pixel accuracy"
      ]
    },
    {
      title: "Real-time Processing",
      points: [
        "60 FPS tracking capability",
        "< 20ms latency",
        "Adaptive calibration",
        "Smooth movement prediction"
      ]
    },
    {
      title: "Privacy First",
      points: [
        "All processing done locally",
        "No data uploaded to servers",
        "Open source codebase",
        "Full user control"
      ]
    }
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
            How It Works
          </h1>
          <p className="text-sm text-neutral-400 max-w-2xl mx-auto">
            Advanced iris and head tracking technology made simple and accessible
          </p>
        </motion.div>

        {/* Process Steps */}
        <div className="mb-16">
          <h2 className="text-xl font-medium mb-8">The Process</h2>
          <div className="space-y-4">
            {steps.map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
                whileHover={{ y: -2, scale: 1.01, transition: { duration: 0.1, ease: 'easeOut' } }}
                className="bg-neutral-900/50 border border-white/10 rounded-2xl p-6 hover:border-white/20 transition-all duration-100"
              >
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0 w-10 h-10 bg-white/5 rounded-xl flex items-center justify-center">
                    <step.icon className="w-5 h-5 text-white" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-xs text-neutral-500">Step {index + 1}</span>
                      <h3 className="text-base font-medium">{step.title}</h3>
                    </div>
                    <p className="text-xs text-neutral-400 leading-relaxed">
                      {step.description}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Technical Features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.5 }}
        >
          <h2 className="text-xl font-medium mb-8">Technical Capabilities</h2>
          <div className="grid md:grid-cols-3 gap-4">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.6 + index * 0.05 }}
                whileHover={{ y: -2, scale: 1.01, transition: { duration: 0.1, ease: 'easeOut' } }}
                className="bg-neutral-900/50 border border-white/10 rounded-2xl p-6 hover:border-white/20 transition-all duration-100"
              >
                <h3 className="text-base font-medium mb-4">{feature.title}</h3>
                <ul className="space-y-2">
                  {feature.points.map((point, i) => (
                    <li key={i} className="text-xs text-neutral-400 flex items-start gap-2">
                      <span className="text-white mt-1">•</span>
                      <span>{point}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* EAR Formula Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.8 }}
          className="mt-16 bg-neutral-900/50 border border-white/10 rounded-2xl p-8 hover:border-white/20 transition-colors duration-200"
        >
          <h2 className="text-xl font-medium mb-4">Eye Aspect Ratio (EAR) Formula</h2>
          <p className="text-sm text-neutral-400 leading-relaxed mb-6">
            Blink detection uses the Eye Aspect Ratio (EAR) formula to measure eye openness in real-time. This algorithm calculates the ratio between eye height and width to detect blinks with high accuracy.
          </p>
          
          <div className="bg-black/50 border border-white/5 rounded-xl p-6 mb-6">
            <div className="text-center mb-4">
              <code className="text-sm font-mono text-white">
                EAR = (||p2 - p6|| + ||p3 - p5||) / (2 × ||p1 - p4||)
              </code>
            </div>
            <div className="grid md:grid-cols-3 gap-4 text-xs text-neutral-400">
              <div>
                <span className="text-white font-medium">p1-p4:</span> Horizontal eye landmarks
              </div>
              <div>
                <span className="text-white font-medium">p2-p6:</span> Vertical landmarks (top-bottom)
              </div>
              <div>
                <span className="text-white font-medium">p3-p5:</span> Vertical landmarks (middle)
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-white/5 rounded-xl p-4">
              <h3 className="text-sm font-medium mb-2">Detection Logic</h3>
              <ul className="text-xs text-neutral-400 space-y-2">
                <li>• Normal eye: EAR ≈ 0.3</li>
                <li>• Closed eye: EAR ≈ 0.1</li>
                <li>• Blink threshold: EAR &lt; 0.2</li>
                <li>• Consecutive frames: 2-3 for validation</li>
              </ul>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <h3 className="text-sm font-medium mb-2">Applications</h3>
              <ul className="text-xs text-neutral-400 space-y-2">
                <li>• Click actions via intentional blinks</li>
                <li>• Drowsiness detection systems</li>
                <li>• Attention monitoring</li>
                <li>• Accessibility control interfaces</li>
              </ul>
            </div>
          </div>
        </motion.div>

        {/* Technology Stack */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.9 }}
          className="mt-16 bg-neutral-900/50 border border-white/10 rounded-2xl p-8 hover:border-white/20 transition-colors duration-200"
        >
          <h2 className="text-xl font-medium mb-4">Built With</h2>
          <p className="text-sm text-neutral-400 leading-relaxed mb-6">
            Blink OS leverages cutting-edge computer vision and machine learning technologies to deliver professional-grade iris and head tracking. Our dual tracking system combines iris precision with head movement detection for natural interaction with digital content.
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {['OpenCV-Python', 'MediaPipe', 'NumPy', 'PyAutoGUI', 'SciPy'].map((tech, index) => (
              <div key={index} className="text-center py-3 bg-white/5 rounded-xl">
                <span className="text-xs font-medium">{tech}</span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
