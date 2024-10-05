import useApiRequest from "app/hooks/useApiRequest.ts";
import api from "app/api";
import {useSelector} from "react-redux";
import {selectCurrentMediaData} from "app/slices/appSlice.ts";
import {useEffect} from "react";

type UseGetAlikeImagesQueryProps = {
    isOpen: boolean;
};

export default function useGetAlikeImagesQuery({isOpen}: UseGetAlikeImagesQueryProps) {
    const currentMediaData = useSelector(selectCurrentMediaData);

    const {trigger, data, isSuccess, isFetching} = useApiRequest({
        apiHook: api.useLazyGetAlikeMediaQuery,
    });

    useEffect(() => {
        if (isOpen && currentMediaData?.file_name) {
            trigger();
        }
    }, [currentMediaData?.file_name, isOpen, trigger]);

    return {data, isSuccess, isFetching};
}
