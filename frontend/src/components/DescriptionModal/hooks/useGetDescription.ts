import useApiRequest from "app/hooks/useApiRequest.ts";
import api from "app/api";
import {useEffect} from "react";
import {useSelector} from "react-redux";
import {selectCurrentMediaData} from "app/slices/appSlice.ts";

export default function useGetDescription({isOpen}: {isOpen: boolean}) {
    const currentMediaData = useSelector(selectCurrentMediaData);
    const {trigger, isFetching} = useApiRequest({
        apiHook: api.useLazyGetDescriptionQuery,
    });

    useEffect(() => {
        if (isOpen) {
            trigger();
        }
    }, [isOpen, trigger, currentMediaData?.file_name]);

    return {
        isFetching,
    };
}
