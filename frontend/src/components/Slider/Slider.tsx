import ReactSlider from 'react-slick';
import { useRef } from 'react';
// @ts-expect-error: Could not find a declaration file for module 'react-use-keypress'.
import useKeypress from 'react-use-keypress';
import { MdErrorOutline } from 'react-icons/md';
import { Spinner } from '@nextui-org/react';

import useAnyModalIsOpen from 'app/hooks/useAnyModalIsOpen.ts';
import useGetCurrentMedia from 'components/Slider/hooks/useGetCurrentMedia.ts';
import useSliderSettings from 'components/Slider/hooks/useSliderSettings.tsx';
import useGetCurrentMediaInfo from 'components/Slider/hooks/useGetCurrentMediaInfo.ts';
import useQuickAccessHotKeys from 'app/hooks/useQuickAccessHotKeys.ts';

export default function Slider() {
    const { url: mediaUrl, isFetching, isError } = useGetCurrentMedia();
    const { isLoading, settings: sliderSettings } = useSliderSettings();
    useGetCurrentMediaInfo();
    useQuickAccessHotKeys();

    const ref = useRef<ReactSlider>(null);
    const isModalOpen = useAnyModalIsOpen();
    const onNext = () => !isModalOpen && ref.current?.slickNext();
    const onPrev = () => !isModalOpen && ref.current?.slickPrev();
    useKeypress('ArrowRight', onNext);
    useKeypress('ArrowLeft', onPrev);

    return (
        <div className="relative">
            <ReactSlider ref={ref} {...sliderSettings}>
                {Array.from({ length: 3 }).map((_, index) => (
                    <div key={index}>
                        <div className="h-[100vh] flex flex-row items-center justify-center">
                            {isFetching || isLoading ? (
                                <div className="w-full h-full flex flex-row justify-center items-center">
                                    <Spinner size="lg" color="primary" />
                                </div>
                            ) : (
                                <img src={mediaUrl} alt="" className="w-auto h-auto max-h-full max-w-full" />
                            )}
                            {isError && (
                                <div className="w-full h-full flex flex-col justify-center items-center">
                                    <MdErrorOutline />
                                    <div>Error loading media, please slide left or right</div>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </ReactSlider>
        </div>
    );
}
