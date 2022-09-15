// -------
// License
// -------
//
// It is released under the MIT license.
//
//     Copyright (c) 2013 Hiroyuki Tanaka
//
//     Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
//
//     The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
//
//     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


#include <stdint.h>
#include <cstdlib>
#include <cstring>
#include <string>
#include <map>
#include <vector>
#include <iostream>
#include <bitset>

#include "./_editdistance.h"

using namespace std;

template<typename T, typename TVALUE>
unsigned int edit_distance_bpv(T &cmap, char const *vec, size_t const &vecsize, unsigned int const &tmax, unsigned int const &tlen) {
    int D = tmax * 64 + tlen;
    TVALUE D0, HP, HN, VP, VN;
    uint64_t top = (1L << (tlen - 1));
    uint64_t lmb = (1L << 63);

    for(size_t i = 0; i <= tmax; ++i) {
        VP[i] = 0;
        VN[i] = 0;
    }
    for(size_t i = 0; i < tmax; ++i) VP[i] = ~0;
    for(size_t i = 0; i < tlen; ++i) VP[tmax] |= (1L << i);
    for(size_t i = 0; i < vecsize; ++i) {
        TVALUE &PM = cmap[vec[i]];
        for(int r = 0; r <= tmax; ++r) {
            uint64_t X = PM[r];
            if(r > 0 && (HN[r - 1] & lmb)) X |= 1L;
            D0[r] = (((X & VP[r]) + VP[r]) ^ VP[r]) | X | VN[r];
            HP[r] = VN[r] | ~(D0[r] | VP[r]);
            HN[r] = D0[r] & VP[r];
            X = (HP[r] << 1L);
            if(r == 0 || HP[r - 1] & lmb) X |= 1L;
            VP[r] = (HN[r] << 1L) | ~(D0[r] | X);
            if(r > 0 && (HN[r - 1] & lmb)) VP[r] |= 1L;
            VN[r] = D0[r] & X;
        }
        if(HP[tmax] & top) ++D;
        else if(HN[tmax] & top) --D;
    }
    return D;
}


/// c.f. http://handasse.blogspot.com/2009/04/c_29.html
template<typename T>
unsigned int edit_distance_dp(T const *str1, size_t const size1, T const *str2, size_t const size2) {
    vector< vector<uint32_t> > d(size1 + 1, vector<uint32_t>(size2 + 1));
    for (int i = 0; i < size1 + 1; i++) d[i][0] = i;
    for (int i = 0; i < size2 + 1; i++) d[0][i] = i;
    for (int i = 1; i < size1 + 1; i++) {
        for (int j = 1; j < size2 + 1; j++) {
            d[i][j] = min(min(d[i-1][j], d[i][j-1]) + 1, d[i-1][j-1] + (str1[i-1] == str2[j-1] ? 0 : 1));
        }
    }
    return d[size1][size2];
}

template <size_t N>
struct varr {
    uint64_t arr_[N];
    uint64_t & operator[](size_t const &i) {
        return arr_[i];
    }
};


template<size_t N>
unsigned int edit_distance_map_(char const *a, size_t const asize, char const *b, size_t const bsize) {
    typedef map<char, varr<N> > cmap_v;
    cmap_v cmap;
    unsigned int tmax = (asize - 1) >> 6;
    unsigned int tlen = asize - tmax * 64;
    for(size_t i = 0; i < tmax; ++i) {
        for(size_t j = 0; j < 64; ++j) cmap[a[i * 64 + j]][i] |= (1L << j);
    }
    for(size_t i = 0; i < tlen; ++i) cmap[a[tmax * 64 + i]][tmax] |= (1L << i);
    return edit_distance_bpv<cmap_v, typename cmap_v::mapped_type>(cmap, b, bsize, tmax, tlen);
}


unsigned int edit_distance(const char *a, const unsigned int asize, const char *b, const unsigned int bsize) {
    if(asize == 0) return bsize;
    else if(bsize == 0) return asize;
    char const *ap, *bp;
    unsigned int const *asizep, *bsizep;
    if(asize < bsize) ap = b, bp = a, asizep = &bsize, bsizep = &asize;
    else ap = a, bp = b, asizep = &asize, bsizep = &bsize;
    size_t vsize = ((*asizep - 1) >> 6) + 1;
    if(vsize > 10) {
        char const *_ = ap;
        unsigned int const *__ = asizep;
        ap = bp, bp = _, asizep = bsizep, bsizep = __;
        vsize = ((*asizep - 1) >> 6) + 1;
    }

    if(vsize == 1) return edit_distance_map_<1>(ap, *asizep, bp, *bsizep);
    else if(vsize == 2) return edit_distance_map_<2>(ap, *asizep, bp, *bsizep);
    else if(vsize == 3) return edit_distance_map_<3>(ap, *asizep, bp, *bsizep);
    else if(vsize == 4) return edit_distance_map_<4>(ap, *asizep, bp, *bsizep);
    else if(vsize == 5) return edit_distance_map_<5>(ap, *asizep, bp, *bsizep);
    else if(vsize == 6) return edit_distance_map_<6>(ap, *asizep, bp, *bsizep);
    else if(vsize == 7) return edit_distance_map_<7>(ap, *asizep, bp, *bsizep);
    else if(vsize == 8) return edit_distance_map_<8>(ap, *asizep, bp, *bsizep);
    else if(vsize == 9) return edit_distance_map_<9>(ap, *asizep, bp, *bsizep);
    else if(vsize == 10) return edit_distance_map_<10>(ap, *asizep, bp, *bsizep);
    return edit_distance_dp<char>(ap, *asizep, bp, *bsizep);
}

int seek_overlap(const char *r1, const int len1, const char *r2, const int len2, const int limit_distance, const int complete_compare_require, const int overlap_require) {

    int overlap_len = 0;
    int offset = 0;

    // forward
    // a match of less than overlap_require is considered as unconfident
    while (offset < len1-overlap_require){
        // the overlap length of r1 & r2 when r2 is move right for offset
        overlap_len = min(len1-offset, len2);

        int diff = 0;
        int i=0;
        for (i=0; i<overlap_len; i++){
            if (r1[offset + i] != r2[i]){
                diff += 1;
                if (diff >= limit_distance && i < complete_compare_require)
                    break;
            }
        }
        
        if (diff < limit_distance || (diff >= limit_distance && i>=complete_compare_require))
            return (offset<<8) + diff;

        offset ++;
    }


    // reverse
    // in this case, the adapter is sequenced since TEMPLATE_LEN < SEQ_LEN
    // check if distance can get smaller if offset goes negative
    // this only happens when insert DNA is shorter than sequencing read length, and some adapter/primer is sequenced but not trimmed cleanly
    // we go reversely
    offset = 0;
    while ( offset > (-(len2-overlap_require)) ) {
        // the overlap length of r1 & r2 when r2 is move right for offset
        overlap_len = min(len1,  len2- abs(offset));

        int diff = 0;
        int i=0;
        for (i=0; i<overlap_len; i++){
            if (r1[i] != r2[-offset + i]) {
                diff += 1;
                if (diff >= limit_distance && i < complete_compare_require)
                    break;
            }
        }
        
        if (diff < limit_distance || (diff >= limit_distance && i>=complete_compare_require))
            return (offset<<8) + diff;

        offset --;
    }
    return 0x7FFFFFFF;
}

// void create_patternmap(PatternMap *pm, char const *a, unsigned int const size) {
//     pm->tmax_ = (size - 1) >> 6;
//     pm->tlen_ = size - pm->tmax_ * 64;
//     for(size_t i = 0; i < pm->tmax_; ++i) {
//         for(size_t j = 0; j < 64; ++j) pm->p_[a[i * 64 + j]][i] |= (1L << j);
//     }
//     for(size_t i = 0; i < pm->tlen_; ++i) pm->p_[a[pm->tmax_ * 64 + i]][pm->tmax_] |= (1L << i);
// }

// unsigned int edit_distance_by_patternmap(PatternMap *pm, const char *b, const unsigned int size) {
//     return edit_distance_bpv<uint64_t[256][4], uint64_t[4]>(pm->p_, b, size, pm->tmax_, pm->tlen_);
// }
