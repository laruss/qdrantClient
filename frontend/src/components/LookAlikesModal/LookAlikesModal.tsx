import {Modal, ModalBody, ModalContent, ModalFooter, ModalHeader} from "@nextui-org/react";
import useLookAlikesModalState from "app/hooks/useLookAlikesModalState.ts";
import ImagePlaceHolder from "components/LookAlikesModal/ImagePlaceHolder.tsx";
import useGetAlikeImagesQuery from "components/LookAlikesModal/hooks/useGetAlikeImagesQuery.ts";
import AlikeImage from "components/LookAlikesModal/AlikeImage.tsx";
import {useEffect, useState} from "react";
import {GetAlikeMediaResponse} from "app/api/generatedApi.ts";
import {useSelector} from "react-redux";
import {selectCurrentMediaData} from "app/slices/appSlice.ts";

export default function LookAlikesModal() {
    const currentMediaData = useSelector(selectCurrentMediaData);
    const [imagesData, setImagesData] = useState<GetAlikeMediaResponse | null>(null);
    const {isOpen, onOpenChange} = useLookAlikesModalState();
    const {data, isFetching} = useGetAlikeImagesQuery({isOpen});

    useEffect(() => {
        setImagesData(null);
    }, [currentMediaData?.file_name]);

    useEffect(() => {
        if (data) {
            setImagesData(data);
        }
    }, [data]);

    return (
        <Modal
            size='full'
            isOpen={isOpen}
            onOpenChange={onOpenChange}
            isDismissable={false}
            classNames={{
                wrapper: 'overflow-hidden',
                body: 'overflow-auto',
            }}
        >
            <ModalContent className='h-full'>
                <ModalHeader className='text-2xl'>
                    Look Alikes
                </ModalHeader>
                <ModalBody className='flex flex-col items-stretch'>
                    <div className='w-full h-full flex flex-row overflow-auto flex-wrap'>
                        {
                            isFetching && Array.from({length: 30}).map((_, index) => (
                                <ImagePlaceHolder key={index}/>
                            ))
                        }
                        {
                            imagesData && imagesData.images.map((imageData, index) => (
                                <AlikeImage images={imageData} key={index}/>
                            ))
                        }
                    </div>
                </ModalBody>
                <ModalFooter/>
            </ModalContent>
        </Modal>
    )
}
