import { TbFileDescription } from 'react-icons/tb';
import { ImCheckboxChecked, ImCheckboxUnchecked } from 'react-icons/im';
import { GrDocumentDownload } from 'react-icons/gr';
import { ControlPanelButtonProps, ControlPanelDataType } from 'components/ControlPanel/types.ts';
import useDescriptionModalState from 'app/hooks/useDescriptionModalState.ts';
import { useEffect, useMemo } from 'react';
import useSetCurrentDataTypeMutation from 'components/ControlPanel/hooks/useSetCurrentDataTypeMutation.ts';
import useDownloadAllImagesDataMutation from 'components/ControlPanel/hooks/useDownloadAllImagesDataMutation.ts';
import useSpinnerModalState from 'app/hooks/useSpinnerModalState.ts';

export default function useControlPanelButtons(controlData: ControlPanelDataType | null) {
    const { downloadAllData, isDownloading, isDownloaded, isError } = useDownloadAllImagesDataMutation();
    const { changeDataType } = useSetCurrentDataTypeMutation();
    const { onOpenChange: onDescriptionModalOpen } = useDescriptionModalState();
    const { onOpenChange: onSpinnerShow } = useSpinnerModalState();

    const currentDataTypeButton = useMemo(() => {
        return controlData?.currentDataType === 'allMedia' ? {
            tooltip: 'All media files are shown',
            icon: ImCheckboxUnchecked,
            label: 'All media files are shown',
            onPress: () => changeDataType({ setDataTypeRequest: { dataType: 'undiscribedMedia' } }),
        } : {
            tooltip: 'Unprocessed media files are shown',
            icon: ImCheckboxChecked,
            label: 'Unprocessed media files are shown',
            onPress: () => changeDataType({ setDataTypeRequest: { dataType: 'allMedia' } }),
        };
    }, [changeDataType, controlData?.currentDataType]);

    useEffect(() => {
        if (isDownloaded || isError) {
            onSpinnerShow(false);
        }
    }, [isDownloaded, isError, onSpinnerShow]);

    useEffect(() => {
        if (isDownloading) {
            onSpinnerShow(true);
        }
    }, [isDownloading, onSpinnerShow]);

    return [
        {
            tooltip: 'Show Description modal',
            icon: TbFileDescription,
            color: 'green',
            label: 'Description modal',
            onPress: () => onDescriptionModalOpen(true),
            isDisabled: !controlData || !controlData.fileName,
        },
        currentDataTypeButton,
        {
            tooltip: 'Download all images JSON data file',
            icon: GrDocumentDownload,
            color: 'blue',
            label: 'Download data',
            onPress: () => {
                downloadAllData();
            },
        },
    ] as Array<ControlPanelButtonProps>;
}
