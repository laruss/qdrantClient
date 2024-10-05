import { generatedApi } from './generatedApi.ts';

const api = generatedApi.enhanceEndpoints({
    addTagTypes: ['Media', 'Config', 'MediaData', 'Description', 'Duplicates'],
    endpoints: {
        getConfig: {
            providesTags: ['Config'],
        },
        getMedia: {
            providesTags: ['Media'],
        },
        getCurrentMediaData: {
            providesTags: ['MediaData'],
        },
        getDescription: {
            providesTags: ['Description'],
        },
        setDescription: {
            invalidatesTags: (_, error) => (error ? [] : ['Description']),
        },
        describeMedia: {
            invalidatesTags: (_, error) => (error ? [] : ['Description']),
        },
        setPromptParts: {
            invalidatesTags: (_, error) => (error ? [] : ['Config']),
        },
        setNextMedia: {
            invalidatesTags: (_, error) => (error ? [] : ['Media', 'MediaData']),
        },
        setPreviousMedia: {
            invalidatesTags: (_, error) => (error ? [] : ['Media', 'MediaData']),
        },
        removeTextFromImage: {
            invalidatesTags: (_, error) => (error ? [] : ['Media']),
        },
        deleteMedia: {
            invalidatesTags: (_, error) => (error ? [] : ['Media', 'MediaData']),
        },
        setDataType: {
            invalidatesTags: (_, error) => (error ? [] : ['Config', 'Media', 'MediaData']),
        },
    },
}) as unknown as typeof generatedApi;

export default api;
