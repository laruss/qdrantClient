import useSpinnerModalState from "app/hooks/useSpinnerModalState.ts";
import useDescribeMutation from "components/DescriptionModal/hooks/useDescribeMutation.ts";
import {useEffect} from "react";

export default function useDescribe() {
    const {onOpenChange: onSpinnerShow} = useSpinnerModalState();
    const {
        describe,
        isDescribing,
        isDescribed,
    } = useDescribeMutation();

    useEffect(() => {
        isDescribing && onSpinnerShow(true);
    }, [isDescribing, onSpinnerShow]);

    useEffect(() => {
        isDescribed && onSpinnerShow(false);
    }, [isDescribed, onSpinnerShow]);

    return describe;
}
