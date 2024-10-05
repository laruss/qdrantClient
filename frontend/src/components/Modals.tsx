import DescriptionModal from 'components/DescriptionModal';
import SpinnerModal from 'components/SpinnerModal.tsx';
import DialogModal from 'components/DialogModal.tsx';
import LookAlikesModal from 'components/LookAlikesModal';

export default function Modals() {
    return (
        <>
            <DescriptionModal/>
            <DialogModal/>
            <LookAlikesModal/>
            <SpinnerModal/>
        </>
    );
}
