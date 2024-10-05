import useApiRequest from 'app/hooks/useApiRequest.ts';
import api from 'app/api';
import { useSelector } from 'react-redux';
import { selectConfig } from 'app/slices/appSlice.ts';
import { useEffect } from 'react';

export default function useGetCurrentMediaInfo() {
    const config = useSelector(selectConfig);

    const { trigger } = useApiRequest({
        apiHook: api.useLazyGetCurrentMediaDataQuery,
    });

    useEffect(() => {
        config && trigger();
    }, [config, trigger]);
}
