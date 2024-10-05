import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

// initialize an empty api service that we'll inject endpoints into later as needed
export const emptySplitApi = createApi({
    baseQuery: fetchBaseQuery({
        baseUrl: import.meta.env.VITE_API_PATH as string,
        responseHandler: async (response) => {
            // image in response.headers.get('content-type')
            if (response.headers.get('content-type')?.includes('image')) {
                const image = await response.blob();

                return {
                    data: image,
                };
            } else if (response.headers.get('content-type')?.includes('application/json')) {
                return await response.json();
            }
        },
    }),
    endpoints: () => ({}),
});
