import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
    const navigate = useNavigate();
    const [activeModule, setActiveModule] = useState(null);

    const modules = [
        { id: 'attendance', name: 'Student Attendance', icon: '🎓', color: 'from-green-500 to-emerald-600' },
        { id: 'headpose', name: 'Head Pose', icon: '🔄', color: 'from-blue-500 to-cyan-600' },
        { id: 'emotion', name: 'Emotion Recognition', icon: '😊', color: 'from-purple-500 to-pink-600' },
        { id: 'handraise', name: 'Hand Raise', icon: '✋', color: 'from-orange-500 to-red-600' }
    ];

    const startModule = (moduleId) => {
        setActiveModule(moduleId);
        // Call Flask API to start module
        fetch(`/start_module/${moduleId}`, { method: 'POST' });
        navigate('/module');
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black p-4">
            <div className="max-w-6xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-center mb-12"
                >
                    <h1 className="text-4xl font-bold text-white mb-2">Welcome, Teacher!</h1>
                    <p className="text-gray-400">Select a module to monitor your classroom</p>
                </motion.div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <AnimatePresence>
                        {modules.map((module) => (
                            <motion.div
                                key={module.id}
                                layout
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                whileHover={{ y: -10 }}
                                className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl p-6 border border-gray-700 cursor-pointer"
                                onClick={() => startModule(module.id)}
                            >
                                <div className={`w-16 h-16 rounded-full bg-gradient-to-r ${module.color} flex items-center justify-center text-2xl mb-4`}>
                                    {module.icon}
                                </div>
                                <h3 className="text-xl font-semibold text-white mb-2">{module.name}</h3>
                                <p className="text-gray-400">Click to start monitoring</p>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                </div>
            </div>
        </div>
    );
}