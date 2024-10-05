import useApiRequest from 'app/hooks/useApiRequest.ts';
import api from 'app/api';

type BeforeChangeProps = {
    currentSlide: number;
    nextSlide: number;
};

export default function useBeforeChange() {
    const { trigger: nextTrigger, isLoading: nextIsLoading } = useApiRequest({
        apiHook: api.useSetNextMediaMutation,
    });

    const { trigger: previousTrigger, isLoading: prevIsLoading } = useApiRequest({
        apiHook: api.useSetPreviousMediaMutation,
    });

    // use the fact that there are 3 slides as placeholders
    return {
        beforeChange: ({ currentSlide, nextSlide }: BeforeChangeProps) => {
            const isSlideLeft =
                (currentSlide === 0 && nextSlide === 2) ||
                (currentSlide === 1 && nextSlide === 0) ||
                (currentSlide === 2 && nextSlide === 1);
            const isSlideRight =
                (currentSlide === 0 && nextSlide === 1) ||
                (currentSlide === 1 && nextSlide === 2) ||
                (currentSlide === 2 && nextSlide === 0);

            if (isSlideLeft) {
                previousTrigger();
            } else if (isSlideRight) {
                nextTrigger();
            }
        },
        isLoading: nextIsLoading || prevIsLoading,
    };
}
