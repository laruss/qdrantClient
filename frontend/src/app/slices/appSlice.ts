import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import {
    AuthorizationModalState,
    ControlPanelState,
    DescriptionModalState,
    DialogModalState,
    DuplicatesModalState,
    LookAlikesModalState,
    SpinnerModalState,
} from 'app/types.ts';
import { RootState } from 'app/store.ts';
import { ConfigValidator, ImageDescription, ImageValidator } from 'app/api/generatedApi.ts';
import api from 'app/api';

export interface AppSlice {
    authorizationModal: AuthorizationModalState;
    controlPanel: ControlPanelState;
    descriptionModal: DescriptionModalState;
    duplicatesModal: DuplicatesModalState;
    lookAlikesModal: LookAlikesModalState;
    dialogModal: DialogModalState;
    spinnerModal: SpinnerModalState;
    config?: ConfigValidator;
    currentMediaData?: ImageValidator;
    descriptionData?: ImageDescription;
}

const initialState: AppSlice = {
    authorizationModal: { isOpen: false },
    controlPanel: { isOpen: false },
    descriptionModal: { isOpen: false },
    duplicatesModal: { isOpen: false },
    lookAlikesModal: { isOpen: false },
    dialogModal: { isOpen: false },
    spinnerModal: { isOpen: false },
};

export const appSlice = createSlice({
    name: 'app',
    initialState,
    reducers: {
        setControlPanelIsOpen(state: AppSlice, action: PayloadAction<boolean>) {
            state.controlPanel.isOpen = action.payload;
        },
        setDescriptionModalIsOpen(state: AppSlice, action: PayloadAction<boolean>) {
            state.descriptionModal.isOpen = action.payload;
        },
        setDuplicatesModalIsOpen(state: AppSlice, action: PayloadAction<boolean>) {
            state.duplicatesModal.isOpen = action.payload;
        },
        setLookAlikesModalIsOpen(state: AppSlice, action: PayloadAction<boolean>) {
            state.lookAlikesModal.isOpen = action.payload;
        },
        setSpinnerModalIsOpen(state: AppSlice, action: PayloadAction<boolean>) {
            state.spinnerModal.isOpen = action.payload;
        },
        setAuthorizationModalIsOpen(state: AppSlice, action: PayloadAction<boolean>) {
            state.authorizationModal.isOpen = action.payload;
        },
        setDialog(state: AppSlice, action: PayloadAction<DialogModalState>) {
            state.dialogModal = action.payload;
        },
        setDescriptionData(state: AppSlice, action: PayloadAction<ImageDescription>) {
            state.descriptionData = action.payload;
        },
    },
    extraReducers: (builder) => {
        builder
            .addMatcher(api.endpoints.getConfig.matchFulfilled, (state, { payload }) => {
                state.config = payload;
            })
            .addMatcher(api.endpoints.getCurrentMediaData.matchFulfilled, (state, { payload }) => {
                state.currentMediaData = payload;
            })
            .addMatcher(api.endpoints.getDescription.matchFulfilled, (state, { payload }) => {
                state.descriptionData = payload;
            });
    },
});

export const {
    setControlPanelIsOpen,
    setDescriptionModalIsOpen,
    setDuplicatesModalIsOpen,
    setLookAlikesModalIsOpen,
    setSpinnerModalIsOpen,
    setAuthorizationModalIsOpen,
    setDialog,
    setDescriptionData,
} = appSlice.actions;

export const selectControlPanel = (state: RootState) => state.app.controlPanel;

export const selectDescriptionModal = (state: RootState) => state.app.descriptionModal;

export const selectDuplicatesModal = (state: RootState) => state.app.duplicatesModal;

export const selectLookAlikesModal = (state: RootState) => state.app.lookAlikesModal;

export const selectSpinnerModal = (state: RootState) => state.app.spinnerModal;

export const selectAuthorizationModal = (state: RootState) => state.app.authorizationModal;

export const selectDialog = (state: RootState) => state.app.dialogModal;

export const selectConfig = (state: RootState) => state.app.config;

export const selectCurrentMediaData = (state: RootState) => state.app.currentMediaData;

export const selectDescriptionData = (state: RootState) => state.app.descriptionData;

export default appSlice.reducer;
