import SliderArrow from 'components/Slider/SliderArrow.tsx';
import { Settings } from 'react-slick';
import useBeforeChange from 'components/Slider/hooks/useBeforeChange.ts';

export default function useSliderSettings() {
    const { isLoading, beforeChange } = useBeforeChange();

    return {
        settings: {
            dots: false,
            infinite: true,
            speed: 500,
            slidesToShow: 1,
            slidesToScroll: 1,
            lazyLoad: 'ondemand',
            prevArrow: <SliderArrow direction="left" className="here-i-go" />,
            nextArrow: <SliderArrow direction="right" />,
            beforeChange(currentSlide: number, nextSlide: number) {
                beforeChange({ currentSlide, nextSlide });
            },
            arrows: true,
        } as Settings,
        isLoading,
    };
}
