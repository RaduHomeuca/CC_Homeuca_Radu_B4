import { Component } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import { Message } from '../hero';
import {CustomersService} from "../services/customers.service";

@Component({
  selector: 'app-get-all-cust-button',
  templateUrl: './get-all-cust-button.component.html',
  styleUrls: ['./get-all-cust-button.component.css']
})

export class GetAllCustButtonComponent {
  message: Message = { message: 1};
  inputField: any;
  inputField2id: any;
  inputField2body: any;
  inputField3id: any;
  inputField3body: any;
  inputField4: any;
  inputField5: any;
  inputField6: any;
  constructor(private http: HttpClient) { }
  getAllCustomers() {
    const data = { message: 'http://localhost:8000/customers' };
    const headers = new HttpHeaders().set('Content-Type', 'application/json');

    this.http.post('http://127.0.0.1:5000/get', JSON.stringify(data), { headers }).subscribe(
      response => {
        console.log(response);
        this.message.message = JSON.stringify(response).slice(1,-1);
      },
      error => {
        console.error(error);
      }
    );


  }
    getSpecificCustomer(id='1') {
    const data = { message: 'http://localhost:8000/customers/'+ id };
    const headers = new HttpHeaders().set('Content-Type', 'application/json');

    this.http.post('http://127.0.0.1:5000/get', JSON.stringify(data), { headers }).subscribe(
      response => {
        console.log(response);
        this.message.message = JSON.stringify(response).slice(1,-1);
      },
      error => {
        console.error(error);
      }
    );

  }

    postSpecificCustomer(id='0', name: "Unknown") {
    const data = { message: 'asd'};
    const headers = new HttpHeaders().set('Content-Type', 'application/json');

    this.http.post('http://127.0.0.1:5000/post/'+ id, JSON.stringify(name), { headers }).subscribe(
      response => {
        console.log(response);
        this.message.message = JSON.stringify(response).slice(1,-1);
      },
      error => {
        console.error(error);
      }
    );

  }
    putSpecificCustomer(id='0', name: "Unknown") {
    const data = { message: 'asd'};
    const headers = new HttpHeaders().set('Content-Type', 'application/json');

    this.http.post('http://127.0.0.1:5000/put/'+ id, JSON.stringify(name), { headers }).subscribe(
      response => {
        console.log(response);
        this.message.message = JSON.stringify(response).slice(1,-1);
      },
      error => {
        console.error(error);
      }
    );

  }
      deleteSpecificCustomer(id='-1') {
    const data = { message: 'http://localhost:8000/customers/'+ id };
    const headers = new HttpHeaders().set('Content-Type', 'application/json');

    this.http.post('http://127.0.0.1:5000/delete', JSON.stringify(data), { headers }).subscribe(
      response => {
        console.log(response);
        this.message.message = JSON.stringify(response).slice(1,-1);
      },
      error => {
        console.error(error);
      }
    );

  }
        getCustomerCompany(id='-1') {
    const data = { message: 'http://localhost:8000/customercif/'+ id };
    const headers = new HttpHeaders().set('Content-Type', 'application/json');

    this.http.post('http://127.0.0.1:5000/cif', JSON.stringify(data), { headers }).subscribe(
      response => {
        console.log(response);
        this.message.message = JSON.stringify(response).slice(1,-1);
      },
      error => {
        console.error(error);
      }
    );

  }
        getCustomerInfo(id='-1') {
    const data = { message: 'http://localhost:8000/customercnp/'+ id };
    const headers = new HttpHeaders().set('Content-Type', 'application/json');

    this.http.post('http://127.0.0.1:5000/cnp', JSON.stringify(data), { headers }).subscribe(
      response => {
        console.log(response);
        this.message.message = JSON.stringify(response).slice(1,-1);
      },
      error => {
        console.error(error);
      }
    );

  }
}

