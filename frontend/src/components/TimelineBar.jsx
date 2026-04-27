import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle2, Circle } from 'lucide-react';

const steps = [
  { id: 'registration', label: 'Registration' },
  { id: 'verification', label: 'Verification' },
  { id: 'campaign', label: 'Campaign' },
  { id: 'voting', label: 'Voting' },
  { id: 'counting', label: 'Counting' },
  { id: 'results', label: 'Results' }
];

const TimelineBar = ({ currentStepIdx }) => {
  return (
    <div className="w-full py-6 px-4 mb-8 overflow-x-auto">
      <div className="flex items-center justify-between min-w-[600px] relative">
        {/* Progress Line */}
        <div className="absolute top-1/2 left-0 w-full h-0.5 bg-slate-800 -translate-y-1/2 z-0" />
        <motion.div 
          className="absolute top-1/2 left-0 h-0.5 bg-indigo-500 -translate-y-1/2 z-0"
          initial={{ width: 0 }}
          animate={{ width: `${(currentStepIdx / (steps.length - 1)) * 100}%` }}
          transition={{ duration: 0.8, ease: "easeInOut" }}
        />

        {steps.map((step, index) => {
          const isCompleted = index < currentStepIdx;
          const isActive = index === currentStepIdx;

          return (
            <div key={step.id} className="relative z-10 flex flex-col items-center gap-2">
              <motion.div
                initial={false}
                animate={{
                  scale: isActive ? 1.2 : 1,
                  backgroundColor: isCompleted || isActive ? '#6366f1' : '#1e293b'
                }}
                className={`w-8 h-8 rounded-full flex items-center justify-center border-2 ${
                  isActive ? 'border-white' : 'border-transparent'
                }`}
              >
                {isCompleted ? (
                  <CheckCircle2 className="w-5 h-5 text-white" />
                ) : (
                  <Circle className={`w-3 h-3 ${isActive ? 'text-white fill-white' : 'text-slate-500'}`} />
                )}
              </motion.div>
              <span className={`text-xs font-medium whitespace-nowrap ${
                isActive ? 'text-white' : 'text-slate-400'
              }`}>
                {step.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TimelineBar;
