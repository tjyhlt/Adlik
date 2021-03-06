// Copyright 2019 ZTE corporation. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0

#ifndef H5B60114C_61E3_4600_971C_356DB8AD102C
#define H5B60114C_61E3_4600_971C_356DB8AD102C

////////////////////////////////////////////////////////////////////////////////
#define __DO_STRINGIZE(s) #s
#define STRINGIZE(s) __DO_STRINGIZE(s)

////////////////////////////////////////////////////////////////////////////////
#define __DO_JOIN_AGAIN(s1, s2) s1##s2
#define __DO_JOIN(s1, s2) __DO_JOIN_AGAIN(s1, s2)

#define JOIN(s1, s2) __DO_JOIN(s1, s2)

////////////////////////////////////////////////////////////////////////////////
#ifdef __COUNTER__
#define UNIQUE_ID __COUNTER__
#else
#define UNIQUE_ID __LINE__
#endif

////////////////////////////////////////////////////////////////////////////////
#define UNIQUE_NAME(prefix) JOIN(prefix, UNIQUE_ID)

#endif
