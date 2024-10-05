import useApiRequest from 'app/hooks/useApiRequest.ts';
import api from 'app/api';
import { useEffect } from 'react';
import { useSelector } from 'react-redux';
import { selectConfig } from 'app/slices/appSlice.ts';

type MediaData = {
    data?: Blob;
};

export default function useGetCurrentMedia() {
    const config = useSelector(selectConfig);

    const { trigger, data, isFetching, isError } = useApiRequest({
        apiHook: api.useLazyGetMediaQuery,
    });
    const mediaData = data as MediaData;

    useEffect(() => {
        config && trigger();
    }, [config, trigger]);

    useEffect(() => {
        // @ts-expect-error: Property 'url' does not exist on type 'Window & typeof globalThis'.
        window.url = mediaData ? URL.createObjectURL(mediaData.data!) : '';
    }, [mediaData]);

    return {
        url: isError ? '' : mediaData ? URL.createObjectURL(mediaData.data!) : '',
        isFetching,
        isError,
    };
}
