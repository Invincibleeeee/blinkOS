import { motion } from 'framer-motion';
import { Eye, Move, Play } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';

export default function Demo() {
  const canvasRef = useRef(null);
  const [activeDemo, setActiveDemo] = useState(null);

  const demos = [
    {
      id: 'iris',
      icon: Eye,
      title: "Iris Gaze Tracking",
      description: "Real-time iris position tracking with sub-pixel precision. Control cursor, click elements, and interact naturally using only your eyes."
    },
    {
      id: 'head',
      icon: Move,
      title: "Head Movement Tracking",
      description: "Natural head movements for scrolling through content. Tilt your head to navigate reels, read PDFs, and browse effortlessly."
    }
  ];

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    let animationFrame;
    let dots = [];

    for (let i = 0; i < 50; i++) {
      dots.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 2 + 1,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        opacity: Math.random() * 0.5 + 0.2
      });
    }

    function animate() {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      dots.forEach(dot => {
        dot.x += dot.vx;
        dot.y += dot.vy;

        if (dot.x < 0 || dot.x > canvas.width) dot.vx *= -1;
        if (dot.y < 0 || dot.y > canvas.height) dot.vy *= -1;

        ctx.beginPath();
        ctx.arc(dot.x, dot.y, dot.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${dot.opacity})`;
        ctx.fill();
      });

      dots.forEach((dot1, i) => {
        dots.slice(i + 1).forEach(dot2 => {
          const dx = dot1.x - dot2.x;
          const dy = dot1.y - dot2.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < 100) {
            ctx.beginPath();
            ctx.moveTo(dot1.x, dot1.y);
            ctx.lineTo(dot2.x, dot2.y);
            ctx.strokeStyle = `rgba(255, 255, 255, ${(1 - distance / 100) * 0.1})`;
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        });
      });

      animationFrame = requestAnimationFrame(animate);
    }

    animate();

    return () => cancelAnimationFrame(animationFrame);
  }, []);

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
            Experience Blink OS
          </h1>
          <p className="text-sm text-neutral-400 max-w-2xl mx-auto">
            See how iris and head tracking technology creates seamless interaction
          </p>
        </motion.div>

        {/* Visualization Canvas */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="relative mb-16 bg-neutral-900/50 border border-white/10 rounded-2xl overflow-hidden"
        >
          <canvas
            ref={canvasRef}
            className="w-full h-96"
            style={{ display: 'block' }}
          />
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="text-center">
              <Eye className="w-12 h-12 text-white/20 mx-auto mb-3" />
              <p className="text-xs text-neutral-500">Live iris tracking visualization</p>
            </div>
          </div>
        </motion.div>

        {/* Demo Cards */}
        <div className="grid md:grid-cols-2 gap-4 mb-16">
          {demos.map((demo, index) => (
            <motion.div
              key={demo.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.2 + index * 0.05 }}
              whileHover={{ y: -2, scale: 1.01, transition: { duration: 0.1, ease: 'easeOut' } }}
              onClick={() => setActiveDemo(activeDemo === demo.id ? null : demo.id)}
              className={`bg-neutral-900/50 border rounded-2xl p-6 cursor-pointer transition-all duration-100 ${
                activeDemo === demo.id ? 'border-white/30' : 'border-white/10 hover:border-white/20'
              }`}
            >
              <demo.icon className="w-5 h-5 text-white mb-4" />
              <h3 className="text-base font-medium mb-2">{demo.title}</h3>
              <p className="text-xs text-neutral-400 leading-relaxed mb-4">
                {demo.description}
              </p>
              <button className="text-xs font-medium flex items-center gap-2 text-white/60 hover:text-white transition-colors duration-200">
                <Play className="w-3 h-3" />
                {activeDemo === demo.id ? 'Demo Active' : 'Try Demo'}
              </button>
            </motion.div>
          ))}
        </div>

        {/* Video Demo Section - Shows when iris tracking is active */}
        {activeDemo === 'iris' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="mb-16 bg-neutral-900/50 border border-white/10 rounded-2xl overflow-hidden"
          >
            <div className="p-6 border-b border-white/10">
              <h3 className="text-base font-medium mb-2">Iris Gaze Tracking Demo</h3>
              <p className="text-xs text-neutral-400">
                Watch how precise iris tracking enables accurate cursor control and interaction
              </p>
            </div>
            <div className="relative bg-black aspect-video">
              <video
                className="w-full h-full object-contain"
                controls
                autoPlay
                loop
                muted
                playsInline
              >
                <source src="/eye.mp4" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          </motion.div>
        )}

        {/* Video Demo Section - Shows when head tracking is active */}
        {activeDemo === 'head' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="mb-16 bg-neutral-900/50 border border-white/10 rounded-2xl overflow-hidden"
          >
            <div className="p-6 border-b border-white/10">
              <h3 className="text-base font-medium mb-2">Head Movement Demo</h3>
              <p className="text-xs text-neutral-400">
                Watch how natural head movements enable smooth scrolling and navigation
              </p>
            </div>
            <div className="relative bg-black aspect-video">
              <video
                className="w-full h-full object-contain"
                controls
                autoPlay
                loop
                muted
                playsInline
              >
                <source src="/head.mp4" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          </motion.div>
        )}

        {/* Getting Started */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.5 }}
          className="bg-neutral-900/50 border border-white/10 rounded-2xl p-8 hover:border-white/20 transition-colors"
        >
          <h2 className="text-xl font-medium mb-4">Ready to Get Started?</h2>
          <p className="text-sm text-neutral-400 leading-relaxed mb-6">
            Blink OS is free and open source. Download now to experience hands-free computer control with precision iris tracking and natural head movement detection.
          </p>
          <div className="flex flex-wrap gap-3">
            <a 
              href="https://github.com/Invincibleeeee/blinkOS"
              target="_blank"
              rel="noopener noreferrer"
            >
              <button className="px-6 py-2.5 bg-white text-black text-sm font-medium rounded-xl hover:bg-neutral-200 transition-colors">
                Download Blink OS
              </button>
            </a>
            <a 
              href="https://github.com/Invincibleeeee/blinkOS"
              target="_blank"
              rel="noopener noreferrer"
            >
              <button className="px-6 py-2.5 bg-white/5 text-white text-sm font-medium rounded-xl hover:bg-white/10 transition-colors border border-white/10">
                View Documentation
              </button>
            </a>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
