/*******************************************************
This program was created by the CodeWizardAVR V3.25 
Automatic Program Generator
© Copyright 1998-2016 Pavel Haiduc, HP InfoTech s.r.l.
http://www.hpinfotech.com

Project : Scoring Board unof
Version : 
Date    : 3/9/2016
Author  : 
Company : 
Comments: 


Chip type               : ATmega8535
Program type            : Application
AVR Core Clock frequency: 11.059200 MHz
Memory model            : Small
External RAM size       : 0
Data Stack size         : 128
*******************************************************/

#include <io.h>
#include <delay.h>
#include <eeprom.h>
#include <string.h>
#include <pgmspace.h>
#include <stdio.h>
#include <mega8535.h>
//#include <interrupt.h>

/*------------------------------------------------------
        Preprocessor UNTUK INTERRUPT USART
------------------------------------------------------*/
#ifndef RXB8
#define RXB8 1
#endif

#ifndef TXB8
#define TXB8 0
#endif

#ifndef UPE
#define UPE 2
#endif

#ifndef DOR
#define DOR 3
#endif

#ifndef FE
#define FE 4
#endif

#ifndef UDRE
#define UDRE 5
#endif

#ifndef RXC
#define RXC 7
#endif

#define FRAMING_ERROR (1<<FE)
#define PARITY_ERROR (1<<UPE)
#define DATA_OVERRUN (1<<DOR)
#define DATA_REGISTER_EMPTY (1<<UDRE)
#define RX_COMPLETE (1<<RXC)

// USART Receiver buffer
#define RX_BUFFER_SIZE 320
char rx_buffer[RX_BUFFER_SIZE];

#if RX_BUFFER_SIZE<256
unsigned char rx_wr_index,rx_rd_index,rx_counter,temp;
#else
unsigned int rx_wr_index,rx_rd_index,rx_counter,temp;
#endif

// This flag is set on USART Receiver buffer overflow
bit rx_buffer_overflow;
unsigned char character_received=0;

/*------------------------------------------------------
        USART Receiver interrupt service routine
------------------------------------------------------*/
interrupt [USART_RXC] void usart_rx_isr(void)
{
char status,data_u;
status=UCSRA;
data_u=UDR;
if ((status & (FRAMING_ERROR | PARITY_ERROR | DATA_OVERRUN))==0)
   {
   character_received=1;
   rx_buffer[rx_wr_index]=data_u;
   if (++rx_wr_index == RX_BUFFER_SIZE) rx_wr_index=0;
   if (++rx_counter == RX_BUFFER_SIZE)
      {
      rx_counter=0;
      rx_buffer_overflow=1;
      };
   };
}

#ifndef _DEBUG_TERMINAL_IO_
// Get a character from the USART Receiver buffer
#define _ALTERNATE_GETCHAR_
#pragma used+
char getchar(void)
{
char data_u;
while (rx_counter==0);
data_u=rx_buffer[rx_rd_index];
if (++rx_rd_index == RX_BUFFER_SIZE) rx_rd_index=0;
#asm("cli")
--rx_counter;
#asm("sei")
return data_u;
}
#pragma used-
#endif

  void clear_buffer(void)
  {  
  //unsigned char temp;
  for (temp=0;temp<RX_BUFFER_SIZE;temp++)
   rx_buffer[temp]=0;           //fils receive buffer at beggining witk x       
   rx_wr_index=0;   //when we empty buffer we should also reset circular buffer pointers to say it is empty.
   rx_rd_index=0;
   rx_counter=0;
  }

/*------------------------------------------------------
        Preprocessor Untuk Shift Register HC595
------------------------------------------------------*/
#define Text_Size 8

//Definisi PORT dan DDR yang digunakan untuk berkomunikasi dengan Shift Register Bagian Kolom(COL) dan Baris(ROW)
#define HC595_COL_PORT    PORTB
#define HC595_COL_DDR     DDRB

//Definisi PIN yang digunakan pada PORT diatas
#define HC595_COL_DS      0
#define HC595_COL_SHCP    1
#define HC595_COL_STCP    2

//Definisi Nilai data HIGH dan LOW pada Shift Register Bagian Kolom(COL) dan Baris(ROW)
#define HC595COL_DataHigh() (HC595_COL_PORT|=(1<<HC595_COL_DS))
#define HC595COL_DataLow()  (HC595_COL_PORT&=(~(1<<HC595_COL_DS)))

//Fungsi Yang Berhubungan Dengan IC 74HC595
void HC595Init(void);
void HC595_Col_Pulse(void);
void HC595_Col_Latch(void);
void Show();

/*------------------------------------------------------
Daftar Inisialisasi variabel global Dalam Program, Beserta Data Type nya, dan Nilai Awalnya
------------------------------------------------------*/
eeprom char Display_Text[] = "00<00801";
eeprom int Display_Column = 5;
volatile int DISP_COL_CNT = 5;

volatile int a=0;
int row=0;
int col=0;

int data;
//int length;
int cepat;
int ms;


//Buffer Text yang akan ditampilkan
char text[] = "00<00801";

//Font Yang Digunakan di dalam Program, yang ditampilkan ke LED Matrix
flash unsigned char smallFont[] =
{
     0x00, // /
     0xFC, // 0
     0x60, // 1
     0xDA, // 2
     0xF2, // 3
     0x66, // 4
     0xB6, // 5
     0xBE, // 6
     0xE0, // 7
     0xFE, // 8
     0xF6, // 9
     0xFC, // : 0
     0x00, // ; blank
     0x0F // <  titik ms
     
};


/*------------------------------------------------------
        Variable USART
------------------------------------------------------*/
flash unsigned char command[] ="HTTP/";
flash unsigned char ipd[] ="+IPD,";
flash unsigned char cek_data[] ="pin=";
flash unsigned char cek_data2[] ="kode=";
flash unsigned char doctype[] ="<!DOCTYPE html>";
flash char reset[] ="<html><p><a href=/?pin=p><button>PLAY</button></a>&nbsp;<a href=/?pin=s><button>STOP</button></a>&nbsp;<a href=/?pin=r><button>RESET</button></a></p><a href=/><h2>";
flash char html[] ="</h2></html>";
flash char gotip[] ="WIFI GOT IP";
flash char sendok[] ="SEND OK";
flash char home[] ="GET / HTTP/1.1";
flash char ready[] ="ready";
//command located in FLASH memory.

unsigned char konek_id[]="0";

/*------------------------------------------------------
        Variable TIMER
------------------------------------------------------*/
unsigned int waktu = 100;
int rubah_waktu = 0;
int cek_wifi = 0;
int set_server = 0;

/*------------------------------------------------------
        Interrupt Timer
------------------------------------------------------*/
// Timer 0 overflow interrupt service routine  UNTUK WAKTU
interrupt [TIM0_OVF] void timer0_ovf_isr(void)
{
// Reinitialize Timer 0 value
TCNT0=0x94;
// Place your code here

rubah_waktu = 1;

}

// Timer1 overflow interrupt service routine    UNTUK CEK WEB SERVER
interrupt [TIM1_OVF] void timer1_ovf_isr(void)
{
// Reinitialize Timer1 value
TCNT1H=0xFF28 >> 8;
TCNT1L=0xFF28 & 0xff;
// Place your code here

cek_wifi = 1;

}

/*------------------------------------------------------
        Fungsi UTAMA
------------------------------------------------------*/
void main(void)
{

   
    //initialisasi USART
    UCSRA=(0<<RXC) | (0<<TXC) | (0<<UDRE) | (0<<FE) | (0<<DOR) | (0<<UPE) | (0<<U2X) | (0<<MPCM);
    UCSRB=(1<<RXCIE) | (0<<TXCIE) | (0<<UDRIE) | (1<<RXEN) | (1<<TXEN) | (0<<UCSZ2) | (0<<RXB8) | (0<<TXB8);
    UCSRC=(1<<URSEL) | (0<<UMSEL) | (0<<UPM1) | (0<<UPM0) | (0<<USBS) | (1<<UCSZ1) | (1<<UCSZ0) | (0<<UCPOL);
    UBRRH=0x00;
    UBRRL=0x05;  // 9600 = 0x47

    ACSR=0x80;
    SFIOR=0x00;

    //initialisasi TIMER0 10ms 
    TCCR0=(0<<WGM00) | (0<<COM01) | (0<<COM00) | (0<<WGM01) | (1<<CS02) | (0<<CS01) | (1<<CS00);
    TCNT0=0x94;
    OCR0=0x00;

    //initialisasi TIMER1 5s
    TCCR1A=(0<<COM1A1) | (0<<COM1A0) | (0<<COM1B1) | (0<<COM1B0) | (0<<WGM11) | (0<<WGM10);
    TCCR1B=(0<<ICNC1) | (0<<ICES1) | (0<<WGM13) | (0<<WGM12) | (1<<CS12) | (0<<CS11) | (1<<CS10);
    TCNT1H=0xFF;
    TCNT1L=0x28;
    ICR1H=0x00;
    ICR1L=0x00;
    OCR1AH=0x00;
    OCR1AL=0x00;
    OCR1BH=0x00;
    OCR1BL=0x00;

    //Inisialisasi DDR yanng terhubung ke IC Shift Reg   
    HC595Init();

    //Ambil nilai jumlah baris dan kolom yang terdapat pada EEPROM, tanpa nilai yang benar, maka display akan kacau
    //eeprom_write_byte(&Display_Column, DISP_COL_CNT);  //untuk PROTEUS ditulis dulu================
    DISP_COL_CNT  = eeprom_read_byte(&Display_Column);

    //Ambil isi teks dari EEPROM
    /*/----------------------------------------
    for(a=0;a<Text_Size;a++)     //untuk PROTEUS ditulis dulu===============
    {
        eeprom_write_byte(&Display_Text[a], text[a]);
    }
    //-----------------------------------------*/
    for(a=0;a<Text_Size;a++)
    {
        text[a] = eeprom_read_byte(&Display_Text[a]); 
    }

    //Ambil panjang dari string 'text'
    //length=strlen(text);   
 //   eeprom_write_byte(&Display_Text[5], 0x38);  
    waktu = 100;
    rubah_waktu = 0;
    cek_wifi = 0;
    set_server = 0;
    cepat = 0;
    ms = 3;  
    if (text[6] == 0x30 && text[7]== 0x30)
                            {
                            cepat = 1;
                            ms = 0;
                            }

    //-------------------Timer(s)/Counter(s) Interrupt(s) initialization
    TIMSK=(0<<OCIE2) | (0<<TOIE2) | (0<<TICIE1) | (0<<OCIE1A) | (0<<OCIE1B) | (1<<TOIE1) | (0<<OCIE0) | (1<<TOIE0);

    //Nyalakan Global Interrupt
    #asm ("sei")
    TCCR0&= (~(1<<CS02 | 1<<CS00));    // Matikan Timer0
    TCCR1B&= (~(1<<CS12 | 1<<CS10));    // Matikan Timer1
    Show();

        delay_ms (3000);
        printf("AT+RST\r\n");

//        delay_ms (5000);
//        printf("AT+CWMODE=3\r\n");

//        delay_ms (5000);
//        printf("AT+CWJAP=\"aMoegan\",\"ibsp2869\"\r\n");

//        delay_ms (15000);
//        printf("AT+CIFSR\r\n");

/*/---------------------------------------- 
    // Reset Source checking
if (MCUCSR & (1<<PORF))
   {
   // Power-on Reset
   MCUCSR&=~((1<<WDRF) | (1<<BORF) | (1<<EXTRF) | (1<<PORF));
   // Place your code here

   }
else if (MCUCSR & (1<<EXTRF))
   {
   // External Reset
   MCUCSR&=~((1<<WDRF) | (1<<BORF) | (1<<EXTRF) | (1<<PORF));
   // Place your code here

   }
//----------------------------------------*/ 
if (MCUCSR & (1<<BORF))
   {
   // Brown-Out Reset
   MCUCSR&=~((1<<WDRF) | (1<<BORF) | (1<<EXTRF) | (1<<PORF));
   // Place your code here
   for(a=0;a<Text_Size;a++)
    {
    text[a] = 0x36;
    }  
    text[5] = 0x38;
    text[2] = 0x3C;
    Show();
   }
else if (MCUCSR & (1<<WDRF))
   {
   // Watchdog Reset
   MCUCSR&=~((1<<WDRF) | (1<<BORF) | (1<<EXTRF) | (1<<PORF));
   // Place your code here
   for(a=0;a<Text_Size;a++)
    {
    text[a] = 0x37;
    }  
    text[5] = 0x38;
    text[2] = 0x3C;
    Show();
   }
//----------------------------------------*/ 
        
// Watchdog Timer initialization
// Watchdog Timer Prescaler: OSC/1024k
#pragma optsize-
#asm("wdr")
WDTCR|=(1<<WDCE) | (1<<WDE);
WDTCR=(0<<WDCE) | (1<<WDE) | (1<<WDP2) | (1<<WDP1) | (1<<WDP0);
#ifdef _OPTIMIZE_SIZE_
#pragma optsize+
#endif


/*------------------------------------------------------
        While UTAMA
------------------------------------------------------*/
while (1)
  {
  #asm("wdr")
if (character_received==1)  //code executes only if something is received
  {   
  character_received=0; 
  if(strstrf(rx_buffer,command))
    {
    konek_id[0] = (*(strstrf(rx_buffer,ipd)+strlenf(ipd))); // ambil data Connection ID
    if(strstrf(rx_buffer,home))
        {
        delay_ms(1);
        printf("AT+CIPSEND=%s,989\r\n",&konek_id);
        delay_ms(1);
        printf(doctype);
        delay_ms(1);
        printf("<html><body><center><head><title>Timer Control anu Unof</title></head><h1>Timer Control anu Unof</h1><h2>Pencet Aja Sesukamu! </h2><button id='p' class='led'>Pencet Play</button><button id='s' class='led'>Pencet Stop</button><button id='r' class='led'>Pencet Reset</button>");
        delay_ms(1);
        printf("<script src='//code.jquery.com/jquery-1.12.0.min.js'></script><script type='text/javascript'>$(document).ready(function(){$('.led').click(function(){var p = $(this).attr('id');$.get('http://172.20.10.2:80/', {kode:p});});});</script>");
        delay_ms(1);
        printf("<h2> </h2><p><a href=/?pin=p><button>PLAY</button></a>&nbsp;<a href=/?pin=s><button>STOP</button></a>&nbsp;<a href=/?pin=r><button>RESET</button></a></p></center>");
        delay_ms(1);
        printf("<center><img src='https://lh3.googleusercontent.com/0iM42AVtd-nrltf9bRsxiULY63eOIaG6v_q-KZGDFQQ=s630-fcrop64=1,00002d8affffeebe'><form action='msg'><p>Type Instruction <input type='text' name='pin' size=50 value='play/stop/reset' autofocus><input type='submit' value='Submit'></form></center></body></html>");

/*                printf("Rx Buffer sebelum clear :");
                puts(rx_buffer) ;
                clear_buffer();
                printf("Rx Buffer sesudah clear :");
                puts(rx_buffer) ;
*/     }
    
    else if(*(strstrf(rx_buffer,cek_data)+strlenf(cek_data))=='r')
        {
                TCCR0&= (~(1<<CS02 | 1<<CS00));    // Matikan Timer0
                for(a=0;a<Text_Size;a++)
                        {
                        text[a] = 0x30;
                        }  
                text[5] = 0x38;
                text[2] = 0x3C;
                ms=3;
                Show();

                delay_ms(1);
                printf("AT+CIPSEND=%s,196\r\n",&konek_id);
                delay_ms(1);
                printf(doctype);
                delay_ms(1);
                printf(reset);
                delay_ms(1);
                printf("RESET!");
                delay_ms(1);
                printf(html);
        }
    
    else if(*(strstrf(rx_buffer,cek_data)+strlenf(cek_data))=='p')
        {
                TCCR0|= (1<<CS02 | 1<<CS00);        // Nyalakan Timer0

                delay_ms(1);
                printf("AT+CIPSEND=%s,196\r\n",&konek_id);
                delay_ms(1);
                printf(doctype);
                delay_ms(1);
                printf(reset); 
                delay_ms(1);
                printf("PLAY !");
                delay_ms(1);
                printf(html);
        }
    else if(*(strstrf(rx_buffer,cek_data)+strlenf(cek_data))=='s')
        {
                TCCR0&= (~(1<<CS02 | 1<<CS00));    // Matikan Timer0
                text[5] = 0x38; 
                Show();

                delay_ms(1);
                printf("AT+CIPSEND=%s,196\r\n",&konek_id);
                delay_ms(1);
                printf(doctype);
                delay_ms(1);
                printf(reset);
                delay_ms(1);
                printf("STOP !");
                delay_ms(1);
                printf(html);
        }

    else if(*(strstrf(rx_buffer,cek_data2)+strlenf(cek_data2))=='s')
        {
                TCCR0&= (~(1<<CS02 | 1<<CS00));    // Matikan Timer0
                text[5] = 0x38;
                Show();

                delay_ms(1);
                printf("AT+CIPCLOSE=%s\r\n",&konek_id);
        }

    else if(*(strstrf(rx_buffer,cek_data2)+strlenf(cek_data2))=='p')
        {
                TCCR0|= (1<<CS02 | 1<<CS00);        // Nyalakan Timer0

                delay_ms(1);
                printf("AT+CIPCLOSE=%s\r\n",&konek_id); 
        }

    else if(*(strstrf(rx_buffer,cek_data2)+strlenf(cek_data2))=='r')
        {
                TCCR0&= (~(1<<CS02 | 1<<CS00));    // Matikan Timer0
                for(a=0;a<Text_Size;a++)
                        {
                        text[a] = 0x30;
                        }
                text[5] = 0x38;
                text[2] = 0x3C;
                text[6] = 0x31; //======================== TES
                ms=3;
                Show();

                delay_ms(1);
                printf("AT+CIPCLOSE=%s\r\n",&konek_id); 
        }

    else if(strstrf(rx_buffer,ipd))  // jika ada kode lain yang diterima
       {
  //      delay_ms(1);
        printf("AT+CIPCLOSE=%s\r\n",&konek_id);
        }   
    clear_buffer();
    }         
    
    if(strstrf(rx_buffer,ready))
        {
        set_server = 0; 
  //      TCCR1B&= (~(1<<CS12 | 1<<CS10));    // Matikan Timer1 ==========untuk Station
        TCCR1B|= (1<<CS12 | 1<<CS10);        // Nyalakan Timer1==========untuk Akses Point
        clear_buffer(); 
        }
    if(strstrf(rx_buffer,sendok))
        {
        printf("AT+CIPCLOSE=%s\r\n",&konek_id);
        clear_buffer(); 
        }
    if(strstrf(rx_buffer,gotip))  // Jika sebagai AP ganti dengan "ready"
        {
        clear_buffer(); 
        TCCR1B|= (1<<CS12 | 1<<CS10);        // Nyalakan Timer1
        }
    if(strstr(rx_buffer,("OK" || "WIFI CONNECTED" || "keep-alive")))
        {
        clear_buffer(); 
        }
  }

if (rubah_waktu == 1)  // Check apakah waktu sudah harus berubah
   {
        rubah_waktu = 0;
        waktu --;
        if (waktu == 0 | waktu == 50 | cepat == 1)       // Show Display
               {
               Show();
               }
        /*------------------------------------------------------
        update variable waktu
        ------------------------------------------------------*/
        text[0]--;
        if (text[0] == 0x2F)  //Satuan 10ms
            {
            text[0] = 0x39;
            text[1]--;
            if (text[1] == 0x34)
               {
               text[5] = 0x3b;   // Titik 2 mati
               }

            if (text[1] == 0x2F)   //Puluhan 10ms
                {
                text[1] = 0x39;
                text[5] = 0x38;  // Titik 2 Hidup
                waktu = 100;     // Reset Counter Waktu
                text[3]--;
                if (text[3] == 0x2F)  //Satuan detik
                    {
                    text[3] = 0x39;
                    text[4]--;
                    if (text[4] == 0x2F)   //Puluhan detik
                        {
                        text[4] = 0x35;

                        if (text[6] == 0x31 && text[7]== 0x30)
                            {
                            cepat = 1;
                            ms = 0;
                            eeprom_write_byte(&Display_Text[6], 0x30);
                            }

                        text[6]--;
                        if (text[6] == 0x2F)   //Satuan menit
                            {
                            text[6] = 0x39;
                            text[7]--;
                            if (text[7] == 0x2F)   //Puluhan menit
                                {
                                text[7] = 0x35; 
                                TCCR0&= (~(1<<CS02 | 1<<CS00));    // Matikan Timer0 
                                cepat = 0;
                                ms = 3;
                                }
                            }
                        }
                    }
                }  
            }
   }

if (cek_wifi == 1)    // Check Wifi, seting Web Server
   {
   cek_wifi = 0;
   set_server++;
   if (set_server == 3)
      {
      printf("AT+CIPMUX=1\r\n");
      }
   else if (set_server == 4)
      {
      printf("AT+CIPSERVER=1,80\r\n");
      }
   else if (set_server == 5)
      {
      printf("AT+CIPSTO=1\r\n");
      set_server = 0;
      TCCR1B&= (~(1<<CS12 | 1<<CS10));    // Matikan Timer1
      }
   }

  } //While Utama
}

/*------------------------------------------------------
       FUNGSI - FUNGSI
------------------------------------------------------*/
void Show()
{
            for(col=(0 + ms);col<(DISP_COL_CNT + ms);col++)
                {
                data=pgm_read_byte( &(smallFont [(text[col]-'/')]));
                eeprom_write_byte(&Display_Text[col], text[col]);  //Simpan di EEPROM
                for(row=0;row<8;row++)
                    {
                    if((data & (1<<row)) != 0)
                    //Jika nilainya == 1
                    HC595COL_DataHigh();
                
                    else
                    //Jika nilainya == 0
                    HC595COL_DataLow();
            
                    HC595_Col_Pulse();
                    }
                }
            //Keluarkan nilai IC Shift Register
            HC595_Col_Latch(); 
}

void HC595Init()
{
    //Ini adalah fungsi untuk menginisialisasi port mikrokontroler yang terhubung dengan Shift Register
    HC595_COL_DDR|=((1<<HC595_COL_SHCP)|(1<<HC595_COL_STCP)|(1<<HC595_COL_DS));    //jadikan sebagai output pada pin yang terkoneksi dengan COL_SHCP,COL_STCP,COL_DS
}

void HC595_Col_Pulse()
{
    //Ini adalah fungsi untuk memberikan clock pada ic Shift Register bagian kolom
    HC595_COL_PORT|=(1<<HC595_COL_SHCP);//HIGH
    HC595_COL_PORT&=(~(1<<HC595_COL_SHCP));//LOW
}

void HC595_Col_Latch()
{
    //Ini adalah fungsi untuk men latch (mengeluarkan) nilai pada ic shift reg bagian kolom
    HC595_COL_PORT|=(1<<HC595_COL_STCP);//HIGH
 //   delay_ms(1);
    HC595_COL_PORT&=(~(1<<HC595_COL_STCP));//LOW
 //   delay_ms(1);
}