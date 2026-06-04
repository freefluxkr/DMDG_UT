import React from 'react';
import { motion } from 'framer-motion';

function SplashIntro() {
  return (
    <motion.div
      initial={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 1.5, ease: "easeInOut" }}
      className="fixed inset-0 z-[100] bg-white flex flex-col items-center justify-center"
    >
      {/* Recreating the logo's colorful paper-cut vortex */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-50">
        <div className="w-[80vw] h-[80vw] max-w-[600px] max-h-[600px] rounded-full border-[40px] border-orange-500 blur-[20px] animate-pulse" />
        <div className="absolute w-[60vw] h-[60vw] max-w-[450px] max-h-[450px] rounded-full border-[30px] border-teal-500 blur-[15px] animate-pulse" style={{ animationDelay: "0.5s" }} />
        <div className="absolute w-[40vw] h-[40vw] max-w-[300px] max-h-[300px] rounded-full border-[20px] border-blue-900 blur-[10px] animate-pulse" style={{ animationDelay: "1s" }} />
      </div>
      
      <motion.div 
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 2, ease: "easeOut" }}
        className="relative z-10 text-center px-4 bg-white/80 p-12 rounded-full backdrop-blur-sm shadow-[0_0_50px_rgba(255,255,255,1)]"
      >
        <motion.h1 
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
          className="serif text-6xl font-bold tracking-[0.4em] text-blue-900 mb-4"
        >
          당목담글
        </motion.h1>
        <p className="text-sm font-bold tracking-[0.3em] text-teal-600 uppercase">
          Connecting Hearts through History
        </p>
        <motion.div 
          initial={{ width: 0 }}
          animate={{ width: "4rem" }}
          transition={{ duration: 1.5, delay: 0.5 }}
          className="h-[2px] bg-orange-500 mx-auto mt-6"
        />
      </motion.div>
    </motion.div>
  );
}

export default SplashIntro;
