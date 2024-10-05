import { useEffect } from 'react';
import { toast } from 'react-toastify';
import {
    TypedUseLazyQuery,
    TypedLazyQueryTrigger,
    BaseQueryFn,
    TypedUseMutation,
    TypedMutationTrigger,
} from '@reduxjs/toolkit/query/react';

type TriggerType<ApiHook, ResultType, QueryArg, BaseQuery extends BaseQueryFn> =
    ApiHook extends TypedUseLazyQuery<ResultType, QueryArg, BaseQuery>
        ? TypedLazyQueryTrigger<ResultType, QueryArg, BaseQuery>
        : ApiHook extends TypedUseMutation<ResultType, QueryArg, BaseQuery>
          ? TypedMutationTrigger<ResultType, QueryArg, BaseQuery>
          : never;

type UseApiRequestProps<ResultType, QueryArg, BaseQuery extends BaseQueryFn> = {
    apiHook: TypedUseLazyQuery<ResultType, QueryArg, BaseQuery> | TypedUseMutation<ResultType, QueryArg, BaseQuery>;
    notifyIfSucceed?: boolean;
    successMessage?: string;
};

type UseApiRequestReturnType<ResultType, QueryArg, BaseQuery extends BaseQueryFn, ApiHook> = {
    trigger: TriggerType<ApiHook, ResultType, QueryArg, BaseQuery>;
    isFetching: boolean;
    isLoading: boolean;
    isError: boolean;
    data: ResultType | undefined;
    isSuccess?: boolean;
};

type UseApiRequestType = <ResultType, QueryArg, BaseQuery extends BaseQueryFn>(
    props: UseApiRequestProps<ResultType, QueryArg, BaseQuery>
) => UseApiRequestReturnType<ResultType, QueryArg, BaseQuery, typeof props.apiHook>;

const useApiRequest: UseApiRequestType = ({ apiHook, notifyIfSucceed, successMessage }) => {
    const [trigger, result] = apiHook();
    const { isFetching, isError, error, data, isSuccess, isLoading } = result;

    useEffect(() => {
        if (isError) {
            console.error(error);
            toast(`Failed to fetch data: ${(error as any)?.data?.message || 'error'}`, { type: 'error' });
        }
    }, [isError, error]);

    useEffect(() => {
        if (notifyIfSucceed && isSuccess) {
            toast(successMessage || 'Data fetched successfully', { type: 'success' });
        }
    }, [isSuccess, notifyIfSucceed, successMessage]);

    return { trigger, isFetching, isLoading, data, isSuccess, isError };
};

export default useApiRequest;
