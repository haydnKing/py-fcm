#pragma once
#include <vector>

//class concurrent_vector;
class CDPResult
{

	public:
  CDPResult(int nclusters, int ncomponents, int npoints,int dimension);
	virtual ~CDPResult(void); 
	int isEM;
	double alpha0; 
	int r;
	
	/* mean values of component/cluster means/covariances */
	int nmcits; // number of mcmc iterations upon which the means are calculated

	vector<RowVector> xmbar;
	vector<RowVector> xmubar;
	RowVector alpha; //J by 1

	#if defined(CDP_TBB)
		concurrent_vector<RowVector> m; //J by D		
		concurrent_vector<SymmetricMatrix> Phi;	//J by D * D
		
		concurrent_vector<RowVector> mu; //(J by T) by D
		concurrent_vector<SymmetricMatrix> Sigma; //(J by T) by (D by D)
		
		concurrent_vector<RowVector> p; //J by T
		concurrent_vector<RowVector> pV; // J by T
	
	    concurrent_vector<RowVector> eta; // J by T 
		
		//work variable
		concurrent_vector<UpperTriangularMatrix> Phi_T_i;   //J by D * D
		concurrent_vector<double> Phi_log_det;
		concurrent_vector<LowerTriangularMatrix> L_i; //(J by T) by (D by D)
		concurrent_vector<double> Sigma_log_det;
	#else
		vector<RowVector> m; //J by D		
		vector<SymmetricMatrix> Phi;	//J by D * D
		
		vector<RowVector> mu; //(J by T) by D
		vector<SymmetricMatrix> Sigma; //(J by T) by (D by D)
		
		vector<RowVector> p; //J by T
		vector<RowVector> pV; // J by T
	
	    vector<RowVector> eta; // J by T 
		
		//work variable
		vector<UpperTriangularMatrix> Phi_T_i;   //J by D * D */
		 vector<double> Phi_log_det; 
		vector<LowerTriangularMatrix> L_i; //(J by T) by (D by D)
		vector<double> Sigma_log_det;
	#endif
	
	int* Z; //N by 1 -- Classification Vector
	int* refZ; //N by 1 -- Reference Classification Vector
	int* refZobs; //T by 1 -- Number of obs in each Classification Component
		
	RowVector q;	// J by 1
	RowVector qV; //J by 1

	int* W; //N by 1
	int* K; //N by 1
	
	inline int GetIndex(int j, int t) {
		return (j * T + t);
	};
	int J;
	int T;
	int N;
	int D;

	// log the current state of the mcmc
	bool SaveW(string FileName);
	bool SaveMu(string FileName);
	bool SaveSigma(string FileName);
	bool SaveK(string FileName);
	bool SaveM(string FileName);
	bool SavePhi(string FileName);
	bool SaveP(string FileName);
	bool SaveQ(string FileName);
	bool SavepV(string FileName);
	bool SaveqV(string FileName);
	bool SaveAlpha(string FileName);
	bool SaveAlpha0(string FileName);
	
	bool SaveEta(string FileName);
	bool SaveZ(string FileName);
	bool SaveFinal();
	
	/* functions to log the *bar values above */
	void UpdateMeans();
	bool SaveXMbar(string FileName);
	bool SaveXMubar(string FileName);
	bool SaveBar();
	void OpenPostFiles();

	/* output files for logging predictive distribution*/
	ofstream postmufile;
	ofstream postpfile;
	ofstream postSigmafile;
	ofstream postmfile;
	ofstream postPhifile;
	ofstream postqfile;
	ofstream postrfile;

	bool SaveDraws();
	bool SavePDraw();
	bool SaveMuDraw();
	bool SaveSigmaDraw();
	bool SaveQDraw();
	bool SaveMDraw();
	bool SavePhiDraw();
	bool SaveRDraw();

};
