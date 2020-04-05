import { Entity, PrimaryGeneratedColumn, Column } from "typeorm";

@Entity()
export class User {

    @PrimaryGeneratedColumn()
    userid:Number;

    @Column()
    username: string;

    @Column()
    emailid: string; 

}