/*
#include <dos.h>
#include <conio.h>
*/

#include <iostream>
#include <stdio.h>
#include <complex>
#include <stdlib.h>
#include <math.h>
#include "RND.H"

//z added
#include <fstream>

using namespace std;
typedef complex<double> cdouble;
#define SWAP(a,b) tempr=(a);(a)=(b);(b)=tempr



cdouble y[20],c[20],p[20][20],ee,b;
int N=13;

int i,j,k,kl,l,m,n,nos,NSYM=700,isign,nn=64;

double pi=4.*atan(1);
double t,Pt;
long int seed;
int ntop=0;
double svk=0.,snk=0.,SNR=0.,BER=0.,sigma=0.001;
double gain=1.05,a0,a1,b0,b1,U,R,hata,data[1000];
cdouble xx[1000],x[1000],v[1000],f[20],h[5],nu,pp[20],cfb[20];
cdouble data1[1000],dataf[64],datap[64],datafu[64],datafuu[64],xu[1000],PN[64],ff[64];
cdouble dataa[64],datab[64],datac[64],datad[64],datae[64];
double amplit[5]={0.227,0.460,0.688,0.460,0.227},alfa[5][8],teta[8],fD=0,Ts=0.0000037,ww=0;
//double amplit[5]={0.4,0.4,0.4,0.2,0.1},alfa[5][8],teta[8],fD=0,Ts=0.0000037,ww=0;

double PN1[64]={1,1,1,1,1,1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,1,1,-1,-1,-1,1,-1,1,-1,-1,
		1,1,1,1,-1,1,-1,-1,-1,1,1,1,-1,-1,1,-1,-1,1,-1,1,1,-1,1,1,1,-1,1,
		1,-1,-1,1,1,-1,1,-1,1,-1,-1};

double sumofpower=0;

void four1(void);
void kal(void);


int main()
{
//z disabled
/*
FILE *canta1;
canta1 = fopen("C:\\ofdm\\papr\\c9.wkr", "w+");
*/

//canta1 = fopen("C:\\cmf.txt", "w+");
//canta1 = fopen("c:\\coding\\coding\\C1.wkr", "w+");

svk=0.;snk=0.;BER=0.;hata=0.; for(i=0;i<N;i++) {f[i]=0.; pp[i]=0.;}

for(i=0;i<5;i++) amplit[i]=amplit[i]/8.0;
for(i=0;i<8;i++) teta[i]=i*2*pi/8.0;


//
for(gain=0.5;gain<=51.0;gain=gain*sqrt(2.0)){/////////////SNR DÖNGÜSÜ//////////////

	seed=-5;
	rnd(&seed);
	seed=14;

	ww=2*pi*fD*Ts;

for(kl=1;kl<6666;kl++){///////////////////KANAL DÖNGÜSÜ/////////////////////
	//5 Taps HiperLAN & WiFi ISI
	//Rayleigh Dante s formulation
	 	for(i=0;i<5;i++){
			for(j=0;j<8;j++) alfa[i][j]=2*pi*rnd(&seed);
		}
		for(i=0;i<5;i++){
			f[i]=0.0001;
			for(j=0;j<8;j++) f[i]=f[i]+polar(amplit[i],alfa[i][j]+1.0*ww*cos(teta[j]));
		//	printf("%d %f %f\n", i, f[i]);getch();
		}
		//Rayleigh sonu


//kanalin frekans ekseni donusumu
		for(i=0;i<64;i++){
			data[2*i+1]=0.0;
			data[2*i+2]=0.0;
		}
		for(i=0;i<5;i++){
			data[2*i+1]=real(f[i]);
			data[2*i+2]=imag(f[i]);
		}

		isign=-1; //ifft
		four1();

		for(i=0;i<64;i++) {
			ff[i].real(data[2*i+1]);
			ff[i].imag(data[2*i+2]);
		}
//kanalin frekans ekseni donusumu


		//datalarin üretilmesi
		for(k=0;k<NSYM;k++){
			data1[k].real(1.0);
			if(rnd(&seed) < 0.5) data1[k].real(-1.0);
			data1[k].imag(1.0);
			if(rnd(&seed) < 0.5) data1[k].imag(-1.0);
		}
		//datalarin üretilmesi sonu
// j sembol index'i
// j yinci sembol kanaldan GECİRİYOR #########################################################################################
for(j=0;j<10;j++){

		for(i=0;i<64;i++){
			data[2*i+1]=real(data1[64*j+i]);
			data[2*i+2]=imag(data1[64*j+i]);
		}

		isign=-1;
		four1();

		for(i=0;i<64;i++){
			dataa[i].real(data[2*i+1]);
			dataa[i].imag(data[2*i+2]);
			}


			m=48;
			for(n=0; n<96;n++)
			{
				x[n]=dataa[m]/64.0;
	//			printf("%4d %7.3f,%7.3f  %7.3f,%7.3f \n",n, x[n], datae[m]); getch();
				m++;
				if (m == 64) m=0;

			}


			for(k=0;k<12;k++){v[k]=0.;y[k]=0.;xu[k]=0.;}

			for(k=5;k<96;k++){
				v[k]=0.;
				for(i=0;i<5;i++) v[k]=v[k]+f[i]*x[k-i];

				R=sqrt(-2.*sigma*log(rnd(&seed)))/gain;
				U=2.*pi*rnd(&seed);
				nu.real(R*cos(U));
				nu.imag(R*sin(U));
				svk=svk+norm(v[k]);
				snk=snk+norm(nu);

				v[k]=v[k]+nu;
//				printf("\n%4d %7.3f,%7.3f ", k, v[k]);getch();
			}

//alinan isaretin frekans ekseni donusumu ve equalization
		for(i=0;i<64;i++){
			data[2*i+1]=real(v[16+i]);
			data[2*i+2]=imag(v[16+i]);
		}

		isign=-1;
		four1();

		for(i=0;i<64;i++) {
			xu[i].real(data[2*i+1]/64.0);
			xu[i].imag(data[2*i+2]/64.0);

			xu[i]=xu[i]/ff[i];
//			printf ("\n %4d %7.3f,%7.3f %7.3f,%7.3f, %7.2f",i, data1[j*64+64-i],xu[i],hata); getch();


		if(real(xu[i]) > 0 && imag(xu[i]) > 0){xu[i].real(1.0);xu[i].imag(1.0);}
		if(real(xu[i]) > 0 && imag(xu[i]) < 0){xu[i].real(1.0);xu[i].imag(-1.0);}
		if(real(xu[i]) < 0 && imag(xu[i]) > 0){xu[i].real(-1.0);xu[i].imag(1.0);}
		if(real(xu[i]) < 0 && imag(xu[i]) < 0){xu[i].real(-1.0);xu[i].imag(-1.0);}

//		printf ("\n %4d %7.3f,%7.3f %7.3f,%7.3f",i, data1[j*64+i],xu[i]); getch();
		if((i >4) && (i < 61) ) {
			ntop++;
			hata=hata+norm(data1[j*64+64-i]-xu[i])/4;
		}
		}//i
//alinan isaretin frekans ekseni donusumu ve equalization

}//j yinci sembolun isi BİTTİ ½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½



}//Kanal Dongu Sonu


	SNR=10.*log10(svk/snk);
	BER=hata/(2.*ntop);
	printf(" SNR=%6.3f     BER=%8.7f\n", SNR,BER);
//z added

//CVS file recording

	ofstream printer("printer.csv");         //Opening file to print info to


    printer<< "'SNR'; 'BER' " << endl;          //Headings for file
    //      cout << "t = " << t << "\t\tF = " << F << endl;
      printer<< "" << SNR << "," << BER << endl;



     printer.close();
}


//END CVS File recording

//z disabled
//	fprintf(canta1, "%6.3f %8.7f\n", SNR,BER);

	svk=0.;snk=0.;BER=0.;hata=0.; ntop=0;
//Gain Dongu Sonu
return 0;
}//Ana Dongu


void four1()
{
	unsigned long n,mmax,m,j,istep,i;
	double wtemp,wr,wpr,wpi,wi,theta;  //Double precision for the
	double tempr,tempi;                 //trigonometric recurrences.

	n=nn << 1;
	j=1;
	for (i=1;i<n;i+=2) {              //This is the bit-reversal section of
		if (j > i){                   //the routine.
			SWAP(data[j],data[i]);    //Exchange the two complex numbers.
			SWAP(data[j+1],data[i+1]);
		}
		m=n >> 1;
		while (m >= 2 && j > m){
			j -= m;
			m >>= 1;
		}
		j += m;
	}
//Here begins the Danielson-Lanczos section of the rotine.
	mmax = 2;
	while (n > mmax){                         //Outer loop executed log2(nn) times.
		istep = mmax << 1;
		theta = isign*(6.28318530717959/mmax);//Initialize the trigonometric
		wtemp = sin(0.5*theta);               //recurrence.
		wpr = -2.0*wtemp*wtemp;
		wpi = sin(theta);
		wr = 1.0;
		wi = 0.0;
		for (m=1;m<mmax;m+=2){       //Here are the two nested inner loops.
			for (i=m;i<=n;i+=istep){
				j = i+mmax;          //This is the Danielson-Lanczos formula.
				tempr = wr*data[j]-wi*data[j+1];
				tempi = wr*data[j+1]+wi*data[j];
				data[j] = data[i]-tempr;
				data[j+1] = data[i+1]-tempi;
				data[i] += tempr;
				data[i+1] += tempi;
			}
			wr = (wtemp=wr)*wpr-wi*wpi+wr; //Trigonometric recurrence.
			wi = wi*wpr+wtemp*wpi+wi;
		}
		mmax = istep;
	}
}


void kal()

{
    cdouble kalman[20],py[20],yp[20],w,ypy;
    int i,j;

	w.real(0.993); w.imag(0.0);

    for(i=0;i<N;i++)
	{
    py[i].real(0);py[i].imag(0);
    for(j=0;j<N;j++)
		{py[i]=py[i]+p[i][j]*conj(y[j]);}
    }
    ypy.real(0); ypy.imag(0);
    for(i=0;i<N;i++)
	{
		ypy=ypy+y[i]*py[i];
    }
    for(i=0;i<N;i++)
	{
		kalman[i]=py[i]/(w+ypy);
    }
    for(i=0;i<N;i++)
	{
    yp[i].real(0);yp[i].imag(0);
    for(j=0;j<N;j++)
		{yp[i]=yp[i]+y[j]*p[j][i];}
    }
    for(i=0;i<N;i++)
	{
    for(j=0;j<N;j++)
		{p[i][j]=(p[i][j]-(kalman[i]*yp[j]))/w;}
    }
    for(i=0;i<N;i++)
	{
    py[i].real(0);py[i].imag(0);
    for(j=0;j<N;j++)
		{py[i]=py[i]+p[i][j]*conj(y[j]);}
    }
    for(i=0;i<N;i++)
	{
		c[i]=c[i]+py[i]*ee;
    }
}
