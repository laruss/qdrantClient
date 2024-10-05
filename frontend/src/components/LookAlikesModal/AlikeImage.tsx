import {FC, useCallback, useState} from 'react';
import { motion } from 'framer-motion';
import {FaDownload, FaExternalLinkAlt} from 'react-icons/fa';
import {Spinner} from "@nextui-org/react";
import {AlikeImage as AlikeImageType} from "app/api/generatedApi.ts";
import useImageLoader from "./hooks/useImageLoader.tsx";
import useOnDownload from "components/LookAlikesModal/hooks/useOnDownload.ts";

interface AlikeImageProps {
    images: AlikeImageType[];
}

const AlikeImage: FC<AlikeImageProps> = ({ images }) => {
    const {Image, size} = useImageLoader({images, className: 'max-w-100 max-h-100'});
    const {isDownloaded, isProcessing, onDownload} = useOnDownload({url: Image.props.src});

    const [isOverlayVisible, setIsOverlayVisible] = useState(false);

    const initialOpacity = (isDownloaded || isProcessing) ? 0.5 : 0;

    const onExternalLinkClick = useCallback((e: React.MouseEvent) => {
        e.stopPropagation();
        window.open(Image.props.src, '_blank');
    }, [Image]);

    const toggleOverlay = useCallback(() => {
        setIsOverlayVisible(prev => !prev);
    }, []);

    const handleDownload = useCallback((e: React.MouseEvent) => {
        e.stopPropagation();
        onDownload();
    }, [onDownload]);

    if (size.height === 0 || size.width === 0) return null;

    return (
        <div className='relative' onClick={toggleOverlay}>
            <motion.div
                className='absolute bg-black w-full h-full flex flex-col justify-center items-center cursor-pointer z-100'
                initial={{opacity: initialOpacity}}
                animate={{opacity: isOverlayVisible ? 1 : initialOpacity}}
                whileHover={{opacity: isOverlayVisible ? 1 : 0.5}}
            >
                <div className='flex flex-row gap-5'>
                    {
                        isProcessing ? (
                            <Spinner size='lg'/>
                        ) : (
                            <>
                                <FaDownload size={36} color={!isDownloaded ? "white" : "green"} onClick={handleDownload}/>
                                <FaExternalLinkAlt size={36} color='white' onClick={onExternalLinkClick}/>
                            </>
                        )
                    }
                </div>
                <div className='text-white opacity-100'>
                    {size.height}x{size.width}
                </div>
            </motion.div>
            {Image}
        </div>
    );
};

export default AlikeImage;
