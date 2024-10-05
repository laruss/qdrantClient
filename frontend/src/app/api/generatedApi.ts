import { emptySplitApi as api } from './emptyApi';
const injectedRtkApi = api.injectEndpoints({
    endpoints: (build) => ({
        getConfig: build.query<GetConfigApiResponse, GetConfigApiArg>({
            query: () => ({ url: `/config` }),
        }),
        setDataType: build.mutation<SetDataTypeApiResponse, SetDataTypeApiArg>({
            query: (queryArg) => ({ url: `/config/dataType`, method: 'POST', body: queryArg.setDataTypeRequest }),
        }),
        setPromptParts: build.mutation<SetPromptPartsApiResponse, SetPromptPartsApiArg>({
            query: (queryArg) => ({ url: `/config/propmts`, method: 'POST', body: queryArg.setPromptPartsPayload }),
        }),
        downloadAllImagesData: build.query<DownloadAllImagesDataApiResponse, DownloadAllImagesDataApiArg>({
            query: () => ({ url: `/data` }),
        }),
        uploadImageData: build.mutation<UploadImageDataApiResponse, UploadImageDataApiArg>({
            query: (queryArg) => ({
                url: `/data`,
                method: 'POST',
                body: queryArg.bodyUploadImageData,
                params: { uploadInQdrant: queryArg.uploadInQdrant },
            }),
        }),
        getDescription: build.query<GetDescriptionApiResponse, GetDescriptionApiArg>({
            query: () => ({ url: `/description` }),
        }),
        setDescription: build.mutation<SetDescriptionApiResponse, SetDescriptionApiArg>({
            query: (queryArg) => ({ url: `/description`, method: 'POST', body: queryArg.imageDescription }),
        }),
        describeMedia: build.mutation<DescribeMediaApiResponse, DescribeMediaApiArg>({
            query: (queryArg) => ({
                url: `/description/describe`,
                method: 'POST',
                body: queryArg.describeMediaPayload,
            }),
        }),
        uploadFaceImage: build.mutation<UploadFaceImageApiResponse, UploadFaceImageApiArg>({
            query: (queryArg) => ({ url: `/files/face`, method: 'POST', body: queryArg.bodyUploadFaceImage }),
        }),
        testFilesTestPost: build.mutation<TestFilesTestPostApiResponse, TestFilesTestPostApiArg>({
            query: (queryArg) => ({ url: `/files/test`, method: 'POST', body: queryArg.bodyTestFilesTestPost }),
        }),
        getImage: build.query<GetImageApiResponse, GetImageApiArg>({
            query: (queryArg) => ({
                url: `/files/images/${queryArg.fileName}`,
                params: { merge_faces: queryArg.mergeFaces },
            }),
        }),
        getCurrentMediaData: build.query<GetCurrentMediaDataApiResponse, GetCurrentMediaDataApiArg>({
            query: () => ({ url: `/media/current/data` }),
        }),
        setNextMedia: build.mutation<SetNextMediaApiResponse, SetNextMediaApiArg>({
            query: () => ({ url: `/media/next`, method: 'POST' }),
        }),
        setPreviousMedia: build.mutation<SetPreviousMediaApiResponse, SetPreviousMediaApiArg>({
            query: () => ({ url: `/media/previous`, method: 'POST' }),
        }),
        getMedia: build.query<GetMediaApiResponse, GetMediaApiArg>({
            query: () => ({ url: `/media/current` }),
        }),
        getAlikeMedia: build.query<GetAlikeMediaApiResponse, GetAlikeMediaApiArg>({
            query: () => ({ url: `/media/alike` }),
        }),
        downloadAlikeMedia: build.mutation<DownloadAlikeMediaApiResponse, DownloadAlikeMediaApiArg>({
            query: (queryArg) => ({
                url: `/media/alike/download`,
                method: 'POST',
                body: queryArg.downloadAlikeMediaBody,
            }),
        }),
        uploadMediaMediaUploadPost: build.mutation<
            UploadMediaMediaUploadPostApiResponse,
            UploadMediaMediaUploadPostApiArg
        >({
            query: (queryArg) => ({
                url: `/media/upload`,
                method: 'POST',
                body: queryArg.bodyUploadMediaMediaUploadPost,
            }),
        }),
        removeTextFromImage: build.mutation<RemoveTextFromImageApiResponse, RemoveTextFromImageApiArg>({
            query: () => ({ url: `/media/text`, method: 'DELETE' }),
        }),
        deleteMedia: build.mutation<DeleteMediaApiResponse, DeleteMediaApiArg>({
            query: () => ({ url: `/media`, method: 'DELETE' }),
        }),
        search: build.mutation<SearchApiResponse, SearchApiArg>({
            query: (queryArg) => ({
                url: `/search`,
                method: 'POST',
                body: queryArg.imageDescription,
                params: { limit: queryArg.limit },
            }),
        }),
    }),
    overrideExisting: false,
});
export { injectedRtkApi as generatedApi };
export type GetConfigApiResponse = /** status 200 Successful Response */ ConfigValidator;
export type GetConfigApiArg = void;
export type SetDataTypeApiResponse = /** status 200 Successful Response */ any;
export type SetDataTypeApiArg = {
    setDataTypeRequest: SetDataTypeRequest;
};
export type SetPromptPartsApiResponse = /** status 200 Successful Response */ any;
export type SetPromptPartsApiArg = {
    setPromptPartsPayload: SetPromptPartsPayload;
};
export type DownloadAllImagesDataApiResponse = /** status 200 Successful Response */ any;
export type DownloadAllImagesDataApiArg = void;
export type UploadImageDataApiResponse = /** status 200 Successful Response */ any;
export type UploadImageDataApiArg = {
    uploadInQdrant?: boolean;
    bodyUploadImageData: BodyUploadImageData;
};
export type GetDescriptionApiResponse = /** status 200 Successful Response */ ImageDescription;
export type GetDescriptionApiArg = void;
export type SetDescriptionApiResponse = /** status 200 Successful Response */ any;
export type SetDescriptionApiArg = {
    imageDescription: ImageDescription;
};
export type DescribeMediaApiResponse = /** status 204 Successful Response */ void;
export type DescribeMediaApiArg = {
    describeMediaPayload: DescribeMediaPayload;
};
export type UploadFaceImageApiResponse = /** status 200 Successful Response */ any;
export type UploadFaceImageApiArg = {
    bodyUploadFaceImage: BodyUploadFaceImage;
};
export type TestFilesTestPostApiResponse = /** status 200 Successful Response */ any;
export type TestFilesTestPostApiArg = {
    bodyTestFilesTestPost: BodyTestFilesTestPost;
};
export type GetImageApiResponse = /** status 200 Successful Response */ any;
export type GetImageApiArg = {
    fileName: string;
    mergeFaces?: boolean;
};
export type GetCurrentMediaDataApiResponse = /** status 200 Successful Response */ ImageValidator;
export type GetCurrentMediaDataApiArg = void;
export type SetNextMediaApiResponse = /** status 200 Successful Response */ any;
export type SetNextMediaApiArg = void;
export type SetPreviousMediaApiResponse = /** status 200 Successful Response */ any;
export type SetPreviousMediaApiArg = void;
export type GetMediaApiResponse = /** status 200 Successful Response */ any;
export type GetMediaApiArg = void;
export type GetAlikeMediaApiResponse = /** status 200 Successful Response */ GetAlikeMediaResponse;
export type GetAlikeMediaApiArg = void;
export type DownloadAlikeMediaApiResponse = /** status 200 Successful Response */ any;
export type DownloadAlikeMediaApiArg = {
    downloadAlikeMediaBody: DownloadAlikeMediaBody;
};
export type UploadMediaMediaUploadPostApiResponse = /** status 200 Successful Response */ any;
export type UploadMediaMediaUploadPostApiArg = {
    bodyUploadMediaMediaUploadPost: BodyUploadMediaMediaUploadPost;
};
export type RemoveTextFromImageApiResponse = /** status 200 Successful Response */ any;
export type RemoveTextFromImageApiArg = void;
export type DeleteMediaApiResponse = unknown;
export type DeleteMediaApiArg = void;
export type SearchApiResponse = /** status 200 Successful Response */ SearchResponse;
export type SearchApiArg = {
    limit?: number | null;
    imageDescription: ImageDescription;
};
export type CurrentDataType = 'allMedia' | 'undiscribedMedia';
export type ConfigValidator = {
    imagesUrlPrefix: string;
    duplicateImagesUrlPrefix?: string;
    currentDataType?: CurrentDataType;
    currentMedia?: string | null;
    promptParts?: string[];
};
export type ValidationError = {
    loc: (string | number)[];
    msg: string;
    type: string;
};
export type HttpValidationError = {
    detail?: ValidationError[];
};
export type SetDataTypeRequest = {
    dataType: CurrentDataType;
};
export type SetPromptPartsPayload = {
    parts: string[];
};
export type BodyUploadImageData = {
    file: Blob;
};
export type ImageDescription = {
    /** The description of the image */
    description: string;
    /** The setting of the image */
    setting: string;
    /** The description of the female in the image */
    femaleDescription: string;
    /** If there is a female in the photo, describe her promiscuity (where promiscuity stands for the totality of the provocativeness of the female's clothing, pose, makeup and other parameters.) */
    femalePromiscuity: string;
    /** The places where the image could be taken */
    places: string[];
    /** The hashtags of the image */
    hashtags: string[];
};
export type DescribeMediaPayload = {
    prompt?: string;
};
export type BodyUploadFaceImage = {
    file: Blob;
};
export type BodyTestFilesTestPost = {
    file: Blob;
};
export type ImageValidator = {
    file_name: string;
    description?: ImageDescription | null;
    hash?: string | null;
    created_at?: string | null;
};
export type AlikeImage = {
    url: string;
    width: number;
    height: number;
};
export type GetAlikeMediaResponse = {
    images: AlikeImage[][];
};
export type DownloadAlikeMediaBody = {
    url: string;
};
export type BodyUploadMediaMediaUploadPost = {
    file: Blob;
};
export type SearchResponse = {
    results: {
        [key: string]: ImageDescription;
    };
};
