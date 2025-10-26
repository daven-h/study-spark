export interface Task {
    id: string;
    title:string;
    estimatePomos?:number
    done:boolean;
    createdAt:string;
    updatedAt:string;
}