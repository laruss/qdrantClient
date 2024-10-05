import { useState, useEffect } from 'react';
import {AlikeImage as AlikeImageType} from "app/api/generatedApi.ts";

type UseImageLoaderProps = {
    images: AlikeImageType[];
    className?: string;
};

type Size = {
    width: number;
    height: number;
};

const useImageLoader = ({ images, className }: UseImageLoaderProps) => {
    const [currentUrl, setCurrentUrl] = useState<string>('');
    const [size, setSize] = useState<Size>({ width: 0, height: 0 });
    const [isLoaded, setIsLoaded] = useState<boolean>(false);

    useEffect(() => {
        let isCancelled = false;

        const loadImage = (url: string, width: number, height: number) => {
            return new Promise<void>((resolve, reject) => {
                const img = new Image();
                img.src = url;
                img.onload = () => {
                    if (!isCancelled) {
                        setCurrentUrl(url);
                        setIsLoaded(true);
                        setSize({ width, height });
                    }
                    resolve();
                };
                img.onerror = () => {
                    reject();
                };
            });
        };

        const tryLoadImages = async () => {
            for (let img of images) {
                try {
                    await loadImage(img.url, img.width, img.height);
                    if (isLoaded) break;
                } catch (error) {
                    console.error(`Failed to load image from ${img.url}:`, error);
                }
            }

            if (!isLoaded && !isCancelled) {
                setCurrentUrl('fake');
            }
        };

        tryLoadImages();

        return () => {
            isCancelled = true;
        };
    }, [images, isLoaded]);

    return {
        Image: <img className={className} src={currentUrl} alt="Loaded content" />,
        size
    };
};

export default useImageLoader;
