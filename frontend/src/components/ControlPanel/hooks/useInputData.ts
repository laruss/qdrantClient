import {ControlPanelDataType} from "components/ControlPanel/types.ts";

export default function useInputData(controlData: ControlPanelDataType | null) {
    if (!controlData) {
        return [];
    }

    return [
        {
            className: 'w-100 opacity-100',
            isDisabled: true,
            label: 'file name',
            value: controlData.fileName
        },
        {
            className: 'w-20 opacity-100',
            isDisabled: true,
            label: 'extension',
            value: controlData.fileExtension
        },
        {
            className: 'w-26 opacity-100',
            isDisabled: true,
            label: 'is described',
            value: controlData.isDescribed,
            color: controlData.isDescribed === 'yes' ? 'success' : 'danger' as 'success' | 'danger'
        }
    ];
}
