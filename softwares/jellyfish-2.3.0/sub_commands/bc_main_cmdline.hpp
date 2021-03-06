/***** This code was generated by Yaggo. Do not edit ******/

/*  This file is part of Jellyfish.

    This work is dual-licensed under 3-Clause BSD License or GPL 3.0.
    You can choose between one of them if you use this work.

`SPDX-License-Identifier: BSD-3-Clause OR  GPL-3.0`
*/

#ifndef __BC_MAIN_CMDLINE_HPP__
#define __BC_MAIN_CMDLINE_HPP__

#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>
#include <getopt.h>
#include <errno.h>
#include <string.h>
#include <stdexcept>
#include <string>
#include <limits>
#include <vector>
#include <iostream>
#include <sstream>
#include <memory>

class bc_main_cmdline {
 // Boiler plate stuff. Conversion from string to other formats
  static bool adjust_double_si_suffix(double &res, const char *suffix) {
    if(*suffix == '\0')
      return true;
    if(*(suffix + 1) != '\0')
      return false;

    switch(*suffix) {
    case 'a': res *= 1e-18; break;
    case 'f': res *= 1e-15; break;
    case 'p': res *= 1e-12; break;
    case 'n': res *= 1e-9;  break;
    case 'u': res *= 1e-6;  break;
    case 'm': res *= 1e-3;  break;
    case 'k': res *= 1e3;   break;
    case 'M': res *= 1e6;   break;
    case 'G': res *= 1e9;   break;
    case 'T': res *= 1e12;  break;
    case 'P': res *= 1e15;  break;
    case 'E': res *= 1e18;  break;
    default: return false;
    }
    return true;
  }

  static double conv_double(const char *str, ::std::string &err, bool si_suffix) {
    char *endptr = 0;
    errno = 0;
    double res = strtod(str, &endptr);
    if(endptr == str) {
      err.assign("Invalid floating point string");
      return (double)0.0;
    }
    if(errno) {
      err.assign(strerror(errno));
      return (double)0.0;
    }
    bool invalid =
      si_suffix ? !adjust_double_si_suffix(res, endptr) : *endptr != '\0';
    if(invalid) {
      err.assign("Invalid character");
      return (double)0.0;
    }
    return res;
  }

  static int conv_enum(const char* str, ::std::string& err, const char* const strs[]) {
    int res = 0;
    for(const char* const* cstr = strs; *cstr; ++cstr, ++res)
      if(!strcmp(*cstr, str))
        return res;
    err += "Invalid constant '";
    err += str;
    err += "'. Expected one of { ";
    for(const char* const* cstr = strs; *cstr; ++cstr) {
      if(cstr != strs)
        err += ", ";
      err += *cstr;
    }
    err += " }";
    return -1;
  }

  template<typename T>
  static bool adjust_int_si_suffix(T &res, const char *suffix) {
    if(*suffix == '\0')
      return true;
    if(*(suffix + 1) != '\0')
      return false;

    switch(*suffix) {
    case 'k': res *= (T)1000; break;
    case 'M': res *= (T)1000000; break;
    case 'G': res *= (T)1000000000; break;
    case 'T': res *= (T)1000000000000; break;
    case 'P': res *= (T)1000000000000000; break;
    case 'E': res *= (T)1000000000000000000; break;
    default: return false;
    }
    return true;
  }

  template<typename T>
  static T conv_int(const char *str, ::std::string &err, bool si_suffix) {
    char *endptr = 0;
    errno = 0;
    long long int res = strtoll(str, &endptr, 0);
    if(endptr == str) {
      err.assign("Invalid signed int string");
      return (T)0;
    }
    if(errno) {
      err.assign(strerror(errno));
      return (T)0;
    }
    bool invalid =
      si_suffix ? !adjust_int_si_suffix(res, endptr) : *endptr != '\0';
    if(invalid) {
      err.assign("Invalid character");
      return (T)0;
    }
    if(res > ::std::numeric_limits<T>::max() ||
       res < ::std::numeric_limits<T>::min()) {
      err.assign("Value out of range");
      return (T)0;
    }
    return (T)res;
  }

  template<typename T>
  static T conv_uint(const char *str, ::std::string &err, bool si_suffix) {
    char *endptr = 0;
    errno = 0;
    while(isspace(*str)) { ++str; }
    if(*str == '-') {
      err.assign("Negative value");
      return (T)0;
    }
    unsigned long long int res = strtoull(str, &endptr, 0);
    if(endptr == str) {
      err.assign("Invalid unsigned int string");
      return (T)0;
    }
    if(errno) {
      err.assign(strerror(errno));
      return (T)0;
    }
    bool invalid =
      si_suffix ? !adjust_int_si_suffix(res, endptr) : *endptr != '\0';
    if(invalid) {
      err.assign("Invalid character");
      return (T)0;
    }
    if(res > ::std::numeric_limits<T>::max()) {
      err.assign("Value out of range");
      return (T)0;
    }
    return (T)res;
  }

  template<typename T>
  static ::std::string vec_str(const std::vector<T> &vec) {
    ::std::ostringstream os;
    for(typename ::std::vector<T>::const_iterator it = vec.begin();
        it != vec.end(); ++it) {
      if(it != vec.begin())
        os << ",";
      os << *it;
    }
    return os.str();
  }

  class string : public ::std::string {
  public:
    string() : ::std::string() {}
    explicit string(const ::std::string &s) : std::string(s) {}
    explicit string(const char *s) : ::std::string(s) {}
    int as_enum(const char* const strs[]) {
      ::std::string err;
      int res = conv_enum((const char*)this->c_str(), err, strs);
      if(!err.empty())
        throw ::std::runtime_error(err);
      return res;
    }


    uint32_t as_uint32_suffix() const { return as_uint32(true); }
    uint32_t as_uint32(bool si_suffix = false) const {
      ::std::string err;
      uint32_t res = conv_uint<uint32_t>((const char*)this->c_str(), err, si_suffix);
      if(!err.empty()) {
        ::std::string msg("Invalid conversion of '");
        msg += *this;
        msg += "' to uint32_t: ";
        msg += err;
        throw ::std::runtime_error(msg);
      }
      return res;
    }
    uint64_t as_uint64_suffix() const { return as_uint64(true); }
    uint64_t as_uint64(bool si_suffix = false) const {
      ::std::string err;
      uint64_t res = conv_uint<uint64_t>((const char*)this->c_str(), err, si_suffix);
      if(!err.empty()) {
        ::std::string msg("Invalid conversion of '");
        msg += *this;
        msg += "' to uint64_t: ";
        msg += err;
        throw ::std::runtime_error(msg);
      }
      return res;
    }
    int32_t as_int32_suffix() const { return as_int32(true); }
    int32_t as_int32(bool si_suffix = false) const {
      ::std::string err;
      int32_t res = conv_int<int32_t>((const char*)this->c_str(), err, si_suffix);
      if(!err.empty()) {
        ::std::string msg("Invalid conversion of '");
        msg += *this;
        msg += "' to int32_t: ";
        msg += err;
        throw ::std::runtime_error(msg);
      }
      return res;
    }
    int64_t as_int64_suffix() const { return as_int64(true); }
    int64_t as_int64(bool si_suffix = false) const {
      ::std::string err;
      int64_t res = conv_int<int64_t>((const char*)this->c_str(), err, si_suffix);
      if(!err.empty()) {
        ::std::string msg("Invalid conversion of '");
        msg += *this;
        msg += "' to int64_t: ";
        msg += err;
        throw ::std::runtime_error(msg);
      }
      return res;
    }
    int as_int_suffix() const { return as_int(true); }
    int as_int(bool si_suffix = false) const {
      ::std::string err;
      int res = conv_int<int>((const char*)this->c_str(), err, si_suffix);
      if(!err.empty()) {
        ::std::string msg("Invalid conversion of '");
        msg += *this;
        msg += "' to int_t: ";
        msg += err;
        throw ::std::runtime_error(msg);
      }
      return res;
    }
    long as_long_suffix() const { return as_long(true); }
    long as_long(bool si_suffix = false) const {
      ::std::string err;
      long res = conv_int<long>((const char*)this->c_str(), err, si_suffix);
      if(!err.empty()) {
        ::std::string msg("Invalid conversion of '");
        msg += *this;
        msg += "' to long_t: ";
        msg += err;
        throw ::std::runtime_error(msg);
      }
      return res;
    }
    double as_double_suffix() const { return as_double(true); }
    double as_double(bool si_suffix = false) const {
      ::std::string err;
      double res = conv_double((const char*)this->c_str(), err, si_suffix);
      if(!err.empty()) {
        ::std::string msg("Invalid conversion of '");
        msg += *this;
        msg += "' to double_t: ";
        msg += err;
        throw ::std::runtime_error(msg);
      }
      return res;
    }
  };

public:
  uint64_t                       size_arg;
  bool                           size_given;
  uint32_t                       mer_len_arg;
  bool                           mer_len_given;
  double                         fpr_arg;
  bool                           fpr_given;
  bool                           canonical_flag;
  uint32_t                       threads_arg;
  bool                           threads_given;
  const char *                   output_arg;
  bool                           output_given;
  uint32_t                       Files_arg;
  bool                           Files_given;
  const char *                   generator_arg;
  bool                           generator_given;
  uint32_t                       Generators_arg;
  bool                           Generators_given;
  const char *                   shell_arg;
  bool                           shell_given;
  const char *                   timing_arg;
  bool                           timing_given;
  ::std::vector<const char *>    file_arg;
  typedef ::std::vector<const char *>::iterator file_arg_it;
  typedef ::std::vector<const char *>::const_iterator file_arg_const_it;

  enum {
    START_OPT = 1000,
    TIMING_OPT
  };

  bc_main_cmdline() :
    size_arg(0), size_given(false),
    mer_len_arg(0), mer_len_given(false),
    fpr_arg((double)0.001), fpr_given(false),
    canonical_flag(false),
    threads_arg((uint32_t)1), threads_given(false),
    output_arg("mer_bloom_filter"), output_given(false),
    Files_arg((uint32_t)1), Files_given(false),
    generator_arg(""), generator_given(false),
    Generators_arg((uint32_t)1), Generators_given(false),
    shell_arg(""), shell_given(false),
    timing_arg(""), timing_given(false),
    file_arg()
  { }

  bc_main_cmdline(int argc, char* argv[]) :
    size_arg(0), size_given(false),
    mer_len_arg(0), mer_len_given(false),
    fpr_arg((double)0.001), fpr_given(false),
    canonical_flag(false),
    threads_arg((uint32_t)1), threads_given(false),
    output_arg("mer_bloom_filter"), output_given(false),
    Files_arg((uint32_t)1), Files_given(false),
    generator_arg(""), generator_given(false),
    Generators_arg((uint32_t)1), Generators_given(false),
    shell_arg(""), shell_given(false),
    timing_arg(""), timing_given(false),
    file_arg()
  { parse(argc, argv); }

  void parse(int argc, char* argv[]) {
    static struct option long_options[] = {
      {"size", 1, 0, 's'},
      {"mer-len", 1, 0, 'm'},
      {"fpr", 1, 0, 'f'},
      {"canonical", 0, 0, 'C'},
      {"threads", 1, 0, 't'},
      {"output", 1, 0, 'o'},
      {"Files", 1, 0, 'F'},
      {"generator", 1, 0, 'g'},
      {"Generators", 1, 0, 'G'},
      {"shell", 1, 0, 'S'},
      {"timing", 1, 0, TIMING_OPT},
      {"help", 0, 0, 'h'},
      {"usage", 0, 0, 'U'},
      {"version", 0, 0, 'V'},
      {0, 0, 0, 0}
    };
    static const char *short_options = "hVUs:m:f:Ct:o:F:g:G:S:";

    ::std::string err;
#define CHECK_ERR(type,val,which) if(!err.empty()) { ::std::cerr << "Invalid " #type " '" << val << "' for [" which "]: " << err << "\n"; exit(1); }
    while(true) {
      int index = -1;
      int c = getopt_long(argc, argv, short_options, long_options, &index);
      if(c == -1) break;
      switch(c) {
      case ':':
        ::std::cerr << "Missing required argument for "
                  << (index == -1 ? ::std::string(1, (char)optopt) : std::string(long_options[index].name))
                  << ::std::endl;
        exit(1);
      case 'h':
        ::std::cout << usage() << "\n\n" << help() << std::endl;
        exit(0);
      case 'U':
        ::std::cout << usage() << "\nUse --help for more information." << std::endl;
        exit(0);
      case 'V':
        print_version();
        exit(0);
      case '?':
        ::std::cerr << "Use --usage or --help for some help\n";
        exit(1);
      case 's':
        size_given = true;
        size_arg = conv_uint<uint64_t>((const char*)optarg, err, true);
        CHECK_ERR(uint64_t, optarg, "-s, --size=uint64")
        break;
      case 'm':
        mer_len_given = true;
        mer_len_arg = conv_uint<uint32_t>((const char*)optarg, err, false);
        CHECK_ERR(uint32_t, optarg, "-m, --mer-len=uint32")
        break;
      case 'f':
        fpr_given = true;
        fpr_arg = conv_double((const char*)optarg, err, false);
        CHECK_ERR(double_t, optarg, "-f, --fpr=double")
        break;
      case 'C':
        canonical_flag = true;
        break;
      case 't':
        threads_given = true;
        threads_arg = conv_uint<uint32_t>((const char*)optarg, err, false);
        CHECK_ERR(uint32_t, optarg, "-t, --threads=uint32")
        break;
      case 'o':
        output_given = true;
        output_arg = optarg;
        break;
      case 'F':
        Files_given = true;
        Files_arg = conv_uint<uint32_t>((const char*)optarg, err, false);
        CHECK_ERR(uint32_t, optarg, "-F, --Files=uint32")
        break;
      case 'g':
        generator_given = true;
        generator_arg = optarg;
        break;
      case 'G':
        Generators_given = true;
        Generators_arg = conv_uint<uint32_t>((const char*)optarg, err, false);
        CHECK_ERR(uint32_t, optarg, "-G, --Generators=uint32")
        break;
      case 'S':
        shell_given = true;
        shell_arg = optarg;
        break;
      case TIMING_OPT:
        timing_given = true;
        timing_arg = optarg;
        break;
      }
    }

    // Check that required switches are present
    if(!size_given)
      error("[-s, --size=uint64] required switch");
    if(!mer_len_given)
      error("[-m, --mer-len=uint32] required switch");

    // Parse arguments
    if(argc - optind < 0)
      error("Requires at least 0 argument.");
    for( ; optind < argc; ++optind) {
      file_arg.push_back(argv[optind]);
    }
  }
  static const char * usage() { return "Usage: jellyfish bc [options] file:path+"; }
  class error {
    int code_;
    std::ostringstream msg_;

    // Select the correct version (GNU or XSI) version of
    // strerror_r. strerror_ behaves like the GNU version of strerror_r,
    // regardless of which version is provided by the system.
    static const char* strerror__(char* buf, int res) {
      return res != -1 ? buf : "Invalid error";
    }
    static const char* strerror__(char* buf, char* res) {
      return res;
    }
    static const char* strerror_(int err, char* buf, size_t buflen) {
      return strerror__(buf, strerror_r(err, buf, buflen));
    }
    struct no_t { };

  public:
    static no_t no;
    error(int code = EXIT_FAILURE) : code_(code) { }
    explicit error(const char* msg, int code = EXIT_FAILURE) : code_(code)
      { msg_ << msg; }
    error(const std::string& msg, int code = EXIT_FAILURE) : code_(code)
      { msg_ << msg; }
    error& operator<<(no_t) {
      char buf[1024];
      msg_ << ": " << strerror_(errno, buf, sizeof(buf));
      return *this;
    }
    template<typename T>
    error& operator<<(const T& x) { msg_ << x; return (*this); }
    ~error() {
      ::std::cerr << "Error: " << msg_.str() << "\n"
                  << usage() << "\n"
                  << "Use --help for more information"
                  << ::std::endl;
      exit(code_);
    }
  };
  static const char * help() { return
    "Create a bloom filter from the input k-mers\n\nHere, a bloom filter is a data structure than can tell if\n" \
    "a k-mer has been since 0 times, once, or at least twice. The data\n" \
    "structure is very memory efficient but has some probability of error.\n" \
    "\n" \
    "After creating the bloom filter, it can be passed to the count\n" \
    "subcommand to avoid counting most k-mers which occur only once.\n\n"
    "Options (default value in (), *required):\n"
    " -s, --size=uint64                       *Expected number of k-mers in input\n"
    " -m, --mer-len=uint32                    *Length of mer\n"
    " -f, --fpr=double                         False positive rate (0.001)\n"
    " -C, --canonical                          Count both strand, canonical representation (false)\n"
    " -t, --threads=uint32                     Number of threads (1)\n"
    " -o, --output=string                      Output file (mer_bloom_filter)\n"
    " -F, --Files=uint32                       Number files open simultaneously (1)\n"
    " -g, --generator=path                     File of commands generating fast[aq]\n"
    " -G, --Generators=uint32                  Number of generators run simultaneously (1)\n"
    " -S, --shell=string                       Shell used to run generator commands ($SHELL or /bin/sh)\n"
    "     --timing=Timing file                 Print timing information\n"
    " -U, --usage                              Usage\n"
    " -h, --help                               This message\n"
    " -V, --version                            Version";
  }
  static const char* hidden() { return ""; }
  void print_version(::std::ostream &os = std::cout) const {
#ifndef PACKAGE_VERSION
#define PACKAGE_VERSION "0.0.0"
#endif
    os << PACKAGE_VERSION << "\n";
  }
  void dump(::std::ostream &os = std::cout) {
    os << "size_given:" << size_given << " size_arg:" << size_arg << "\n";
    os << "mer_len_given:" << mer_len_given << " mer_len_arg:" << mer_len_arg << "\n";
    os << "fpr_given:" << fpr_given << " fpr_arg:" << fpr_arg << "\n";
    os << "canonical_flag:" << canonical_flag << "\n";
    os << "threads_given:" << threads_given << " threads_arg:" << threads_arg << "\n";
    os << "output_given:" << output_given << " output_arg:" << output_arg << "\n";
    os << "Files_given:" << Files_given << " Files_arg:" << Files_arg << "\n";
    os << "generator_given:" << generator_given << " generator_arg:" << generator_arg << "\n";
    os << "Generators_given:" << Generators_given << " Generators_arg:" << Generators_arg << "\n";
    os << "shell_given:" << shell_given << " shell_arg:" << shell_arg << "\n";
    os << "timing_given:" << timing_given << " timing_arg:" << timing_arg << "\n";
    os << "file_arg:" << vec_str(file_arg) << "\n";
  }
};
#endif // __BC_MAIN_CMDLINE_HPP__"
