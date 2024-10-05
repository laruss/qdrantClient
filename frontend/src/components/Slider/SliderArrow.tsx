import { CSSProperties } from 'react';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';
import useAnyModalIsOpen from 'app/hooks/useAnyModalIsOpen.ts';

type SliderArrowProps = {
    direction: 'left' | 'right';
    style?: CSSProperties;
    className?: string;
    onClick?: () => void;
};

export default function SliderArrow({ direction, onClick }: SliderArrowProps) {
    const isModalOpen = useAnyModalIsOpen();
    const Icon = direction === 'left' ? FaChevronLeft : FaChevronRight;
    const arrowStyles = direction === 'left' ? 'left-0' : 'right-0';

    if (isModalOpen) return null;

    return (
        <Icon
            onClick={onClick}
            className={`z-100 color-black opacity-50 hover:opacity-30 active:opacity-10 active:scale-105 w-20 h-20 max-w-20 max-h-20 absolute cursor-pointer top-1/2 ${arrowStyles}`}
        />
    );
}
