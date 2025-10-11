import { DateTime } from 'luxon';

export type ResultData = {
    id: number;
    datasetName: string;
    dateUploaded: DateTime;
    numberOfRows: number;
    numberOfRowsWithErrors: number;
    numberOfUniqueCats: number;
}