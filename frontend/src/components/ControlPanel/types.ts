import type {IconType} from "react-icons";
import {CurrentDataType} from "app/api/generatedApi.ts";

export type ControlPanelButtonProps = {
    icon: IconType;
    label: string;
    onPress: () => unknown;
    color: string;
    tooltip: string;
};

export type ControlPanelDataType = {
    fileName: string;
    fileExtension: string;
    isDescribed: 'yes' | 'no';
    currentDataType: CurrentDataType
}
