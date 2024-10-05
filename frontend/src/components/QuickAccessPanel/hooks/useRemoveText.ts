import useApiRequest from "app/hooks/useApiRequest.ts";
import api from "app/api";
import useSpinnerModalState from "app/hooks/useSpinnerModalState.ts";
import {useEffect} from "react";

export default function useRemoveText() {
    const {onOpenChange: onSpinnerShow} = useSpinnerModalState();

    const {trigger, isLoading, isSuccess, isError} = useApiRequest({
        apiHook: api.useRemoveTextFromImageMutation,
    });

    useEffect(() => {
        isLoading && onSpinnerShow(true);
    }, [onSpinnerShow, isLoading]);

    useEffect(() => {
        (isSuccess || isError) && onSpinnerShow(false);
    }, [onSpinnerShow, isError, isSuccess]);

    return trigger;
}
