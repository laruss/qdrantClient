import { useState, useRef, useEffect, FC } from 'react';
import {motion, AnimatePresence} from 'framer-motion';
import {FaBars} from 'react-icons/fa';
import {Tooltip} from "@nextui-org/react";
import useQuickAccessIconButtons from "components/QuickAccessPanel/hooks/useQuickAccessIconButtons.ts";

const QuickAccessPanel: FC = () => {
    const [isOpen, setIsOpen] = useState(false);
    const panelRef = useRef<HTMLDivElement>(null);
    const iconButtons = useQuickAccessIconButtons();

    const onIconClick = (callback: CallableFunction) => {
        setIsOpen(false);
        callback();
    };

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (panelRef.current && !panelRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const togglePanel = () => setIsOpen(!isOpen);

    return (
        <div ref={panelRef} className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50">
            <motion.button
                onClick={togglePanel}
                className="text-black bg-white bg-opacity-20 rounded-full p-3 shadow-lg"
                whileHover={{scale: 1.1}}
                whileTap={{scale: 0.9}}
            >
                <FaBars className="w-6 h-6"/>
            </motion.button>
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{opacity: 0, scaleX: 0}}
                        animate={{opacity: 1, scaleX: 1}}
                        exit={{opacity: 0, scaleX: 0}}
                        className="absolute top-16 left-1/2 -m-l-30 transform -translate-x-1/2 bg-white bg-opacity-50 rounded-lg shadow-xl p-2 flex space-x-2"
                    >
                        {iconButtons.map(({icon: Icon, ...props}) => (
                            <Tooltip key={props.label} content={props.tooltip}>
                                <div>
                                    <motion.button
                                        className="bg-gray-100 text-gray-800 rounded-full p-3 hover:bg-gray-200"
                                        whileHover={{scale: 1.1}}
                                        whileTap={{scale: 0.9}}
                                        onClick={() => onIconClick(props.callback)}
                                    >
                                        <Icon className="w-6 h-6" color={props.color}/>
                                    </motion.button>
                                </div>
                            </Tooltip>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default QuickAccessPanel;
