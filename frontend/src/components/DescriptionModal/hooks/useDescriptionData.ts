import { ChangeEvent, useCallback, useMemo } from 'react';
import {useDispatch, useSelector} from "react-redux";
import {selectDescriptionData, setDescriptionData} from "app/slices/appSlice.ts";
import {ImageDescription} from "app/api/generatedApi.ts";

type OnDataChangeProps = {
    fieldName: 'description' | 'setting' | 'femaleDescription' | 'femalePromiscuity' | 'places' | 'hashtags';
    value: string | Array<string>;
};

export default function useDescriptionData() {
    const dispatch = useDispatch();
    const descriptionData = useSelector(selectDescriptionData);

    const onDataChange = useCallback(({fieldName, value}: OnDataChangeProps) => {
        dispatch(setDescriptionData({
            ...descriptionData,
            [fieldName]: value,
        } as ImageDescription));
    }, [descriptionData, dispatch]);

    return useMemo(() => ([
        {
            name: 'description',
            label: 'Description',
            value: descriptionData?.description || '',
            onChange: (e: ChangeEvent<HTMLInputElement>) => onDataChange({
                fieldName: 'description',
                value: e.target.value,
            }),
        },
        {
            name: 'setting',
            label: 'Setting',
            value: descriptionData?.setting || '',
            onChange: (e: ChangeEvent<HTMLInputElement>) => onDataChange({
                fieldName: 'setting',
                value: e.target.value,
            }),
        },
        {
            name: 'femaleDescription',
            label: 'Female Description',
            value: descriptionData?.femaleDescription || '',
            onChange: (e: ChangeEvent<HTMLInputElement>) => onDataChange({
                fieldName: 'femaleDescription',
                value: e.target.value,
            }),
        },
        {
            name: 'femalePromiscuity',
            label: 'Female Promiscuity',
            value: descriptionData?.femalePromiscuity || '',
            onChange: (e: ChangeEvent<HTMLInputElement>) => onDataChange({
                fieldName: 'femalePromiscuity',
                value: e.target.value,
            }),
        },
        {
            name: 'places',
            label: 'Places',
            value: descriptionData?.places || [],
            onChange: (values: Array<string>) => onDataChange({
                fieldName: 'places',
                value: values,
            }),
        },
        {
            name: 'hashtags',
            label: "Hash Tags",
            value: descriptionData?.hashtags || [],
            onChange: (values: Array<string>) => onDataChange({
                fieldName: 'hashtags',
                value: values,
            }),
        }
    ]), [descriptionData, onDataChange]);
}
