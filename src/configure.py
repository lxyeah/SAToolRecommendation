import os

# github上项目名称
pro_name = 'commons-net'

root_dir = 'E:/SAToolRecommendation/Bug-Assessment-Tool/'

report_path = 'E:/SAToolRecommendation/reports/'
data_dir = root_dir + '/data/'

tool_evaluation_path = 'E:/SAToolRecommendation/Bug-Assessment-Tool/tool_evaluation_result'

# 本地项目路径
base_pro_path = '/repos/'
repo_path = root_dir + base_pro_path + "/"

# 输出文件保存路径
base_res_path = '/results/'
res_path = root_dir + base_res_path + '/'

xml_res = '/xml_res/'
csv_res = '/csv_res/'

checkstyle_res_path = '/checkstyle_res/'
checkstyle_xml_res_path = checkstyle_res_path + xml_res
checkstyle_csv_res_path = checkstyle_res_path + csv_res

findbugs_res_path = '/findbugs_res/'
classes_repo = '/classes_repo/'
findbugs_classes_repo_path = findbugs_res_path + classes_repo
findbugs_xml_res_path = findbugs_res_path + xml_res
findbugs_csv_res_path = findbugs_res_path + csv_res

pmd_res_path = '/pmd_res/'
pmd_xml_res_path = pmd_res_path + xml_res
pmd_csv_res_path = pmd_res_path + csv_res

# SATools路径
bas_tool_path = '/SATools/'
tool_path = root_dir + bas_tool_path + '/'

checkstyle_path = tool_path + '/checkstyle/'
jar_path = checkstyle_path + 'checkstyle-9.1-all.jar'
rules_path = checkstyle_path + '/rules/'
google_checks_path = rules_path + 'google_checks.xml'
sun_checks_path = rules_path + 'sun_checks.xml'

pmd_path = tool_path + '/pmd/'
pmd_rules_path = pmd_path + '/rules/'
pmd_rule_xml_path = pmd_rules_path + '/rules.xml'

# 类型映射表路径
base_type_uniform_path = 'type_uniform/'
type_uniform_path = root_dir + base_type_uniform_path

type_uniform_html_path = type_uniform_path + '/asat-gdc-mapping.html'

type_uniform_table_path = type_uniform_path + '/tables/'
type_uniform_checkstyle_table_path = type_uniform_table_path + '/checkstyle/'
type_uniform_findbugs_table_path = type_uniform_table_path + '/findbugs/'
type_uniform_pmd_table_path = type_uniform_table_path + '/pmd/'

type_uniform_uniform_path = type_uniform_path + '/uniform/'
type_uniform_checkstyle_uniform_path = type_uniform_uniform_path + '/checkstyle/'
type_uniform_findbugs_uniform_path = type_uniform_uniform_path + '/findbugs/'
type_uniform_pmd_uniform_path = type_uniform_uniform_path + '/pmd/'

# uniform表相关配置
uniform_head = ['file_path', 'start', 'type']
map_table_index = {
    'Rule name': 0,
    'Classification': 1
}
findbugs_index = {
    'method_name': 0,
    'method_sig': 1,
    'file_path': 2,
    'class_name': 3,
    'lstart': 4,
    'lend': 5,
    'priority': 6,
    'category': 7
}
checkstyle_index = {
    'file': 0,
    'line': 1,
    'severity': 2,
    'message': 3,
    'source': 4
}
pmd_index = {
    'Problem': 0,
    'Package': 1,
    'File': 2,
    'Priority': 3,
    'Line': 4,
    'Description': 5,
    'Rule set': 6,
    'Rule': 7
}

now_pro_path = os.getcwd().replace('/', '/').split('src')[0]

data_repo = 'E:/data_repo/'
data_info = 'E:/data_info/'
init_data = data_info + 'init_data/'
projects = data_info + 'projects/'

unzip_repo = '/unzip_repos/'
zip_repo = '/zip_repos/'

start_label = 65
tag_num = 15
start_revision = 'Tue Jan 1 00:00:00 2013'
revision_interval = 90

feature_dir = 'D:/graduated/exp/metrics/'

feature_index = {
    'Kind': 0,
    'Name': 1,
    'File': 2,
    'AvgCyclomatic': 3,
    'AvgCyclomaticModified': 4,
    'AvgCyclomaticStrict': 5,
    'AvgEssential': 6,
    'AvgLine': 7,
    'AvgLineBlank': 8,
    'AvgLineCode': 9,
    'AvgLineComment': 10,
    'CountClassBase': 11,
    'CountClassCoupled': 12,
    'CountClassCoupledModified': 13,
    'CountClassDerived': 14,
    'CountDeclClass': 15,
    'CountDeclClassMethod': 16,
    'CountDeclClassVariable': 17,
    'CountDeclExecutableUnit': 18,
    'CountDeclFile': 19,
    'CountDeclFunction': 20,
    'CountDeclInstanceMethod': 21,
    'CountDeclInstanceVariable': 22,
    'CountDeclMethod': 23,
    'CountDeclMethodAll': 24,
    'CountDeclMethodDefault': 25,
    'CountDeclMethodPrivate': 26,
    'CountDeclMethodProtected': 27,
    'CountDeclMethodPublic': 28,
    'CountInput': 29,
    'CountLine': 30,
    'CountLineBlank': 31,
    'CountLineCode': 32,
    'CountLineCodeDecl': 33,
    'CountLineCodeExe': 34,
    'CountLineComment': 35,
    'CountOutput': 36,
    'CountPath': 37,
    'CountPathLog': 38,
    'CountSemicolon': 39,
    'CountStmt': 40,
    'CountStmtDecl': 41,
    'CountStmtExe': 42,
    'Cyclomatic': 43,
    'CyclomaticModified': 44,
    'CyclomaticStrict': 45,
    'Essential': 46,
    'Knots': 47,
    'MaxCyclomatic': 48,
    'MaxCyclomaticModified': 49,
    'MaxCyclomaticStrict': 50,
    'MaxEssential': 51,
    'MaxEssentialKnots': 52,
    'MaxInheritanceTree': 53,
    'MaxNesting': 54,
    'MinEssentialKnots': 55,
    'PercentLackOfCohesion': 56,
    'PercentLackOfCohesionModified': 57,
    'RatioCommentToCode': 58,
    'SumCyclomatic': 59,
    'SumCyclomaticModified': 60,
    'SumCyclomaticStrict': 61,
    'SumEssential': 62
}

feature_type_dic = {
    'File': ['File'],
    'Class': ['Anonymous Class', 'Public Class', 'Public Generic Class', 'Public Interface', 'Public Generic Interface'],
    'Package': ['Package'],
    'Method': ['Abstract Method', 'Abstract Method', 'Constructor', 'Method', 'Private Generic Method', 'Private Method',
               'Private Static Method', 'Protected Constructor', 'Protected Generic Method', 'Protected Method', 'Public Abstract Method',
               'Public Constructor', 'Public Generic Method', 'Public Method', 'Public Static Generic Method', 'Public Static Method']
}

feature_type_num_dic = {
    'File': 40,
    'Package': 39,
    'Class': 45,
    'Method': 27
}

fileMap = {"category_line": 0,
           "vtype_line": 1,
           "priority_line": 2,
           "rank_line": 3,
           "project_line": 4,
           "rootId_line": 5,
           'buggy_line': 6,
           "file_line": 7,
           "leafId_line": 10,
           "file_path_line": 11,
           "method_line": 12,
           "field_line": 13,
           "resolution_line": 14,
           "life_time_line": 15}

categroyMap = {'B': "BAD_PRACTICE",
               'C': "CORRECTNESS",
               "E": "Malicious code vulnerability",
               'I': "I18N",
               'D': "DODGY_CODE",
               'S': "SECURITY",
               'P': "PERFORMANCE",
               'V': "MALICIOUS_CODE",
               'X': "EXPERIMENTAL",
               'M': "Multithreaded correctness"
               }

init_file_headers = [
    "categpry", "vtype", "priority", "rank", "project", 'origin commit', 'buggy commit', 'buggy path', 'buggy start',
    "buggy end", "fixer", "fixer path", 'method', 'field', 'resolution']

metrics_headers = "Kind,Name,File,AvgCyclomatic,AvgCyclomaticModified,AvgCyclomaticStrict,AvgEssential," \
                  "AvgLine,AvgLineBlank,AvgLineCode,AvgLineComment,CountClassBase,CountClassCoupled," \
                  "CountClassCoupledModified,CountClassDerived,CountDeclClass,CountDeclClassMethod," \
                  "CountDeclClassVariable,CountDeclExecutableUnit,CountDeclFile,CountDeclFunction," \
                  "CountDeclInstanceMethod,CountDeclInstanceVariable,CountDeclMethod,CountDeclMethodAll," \
                  "CountDeclMethodDefault,CountDeclMethodPrivate,CountDeclMethodProtected,CountDeclMethodPublic," \
                  "CountInput,CountLine,CountLineBlank,CountLineCode,CountLineCodeDecl,CountLineCodeExe," \
                  "CountLineComment,CountOutput,CountPath,CountPathLog,CountSemicolon,CountStmt,CountStmtDecl," \
                  "CountStmtExe,Cyclomatic,CyclomaticModified,CyclomaticStrict,Essential,Knots,MaxCyclomatic," \
                  "MaxCyclomaticModified,MaxCyclomaticStrict,MaxEssential,MaxEssentialKnots,MaxInheritanceTree," \
                  "MaxNesting,MinEssentialKnots,PercentLackOfCohesion,PercentLackOfCohesionModified," \
                  "RatioCommentToCode,SumCyclomatic,SumCyclomaticModified,SumCyclomaticStrict,SumEssential".split(",")
metricsMap = {
    "kind": 0,
    "fileName": 1,
    "startNums": 2
}

pmd_category_list = ['Design', 'Performance', 'Best Practices', 'Error Prone', 'Multithreading', 'Security', 'Ruleset']

pmd_vtype_list = ['ImmutableField', 'InsufficientStringBufferDeclaration', 'ConsecutiveLiteralAppends', 'ConsecutiveAppendsShouldReuse', 'AppendCharacterWithChar', 'GuardLogStatement', 'NullAssignment', 'CouplingBetweenObjects', 'AbstractClassWithoutAbstractMethod', 'TooManyMethods', 'MutableStaticState', 'MissingOverride', 'ClassCastExceptionWithToArray', 'UseConcurrentHashMap', 'AvoidInstantiatingObjectsInLoops', 'GodClass', 'UseLocaleWithCaseConversions', 'ExceptionAsFlowControl', 'PreserveStackTrace', 'LiteralsFirstInComparisons', 'AvoidCatchingGenericException', 'AvoidThrowingRawExceptionTypes', 'UnusedAssignment', 'AvoidAccessibilityAlteration', 'CollapsibleIfStatements', 'AvoidDuplicateLiterals', 'CyclomaticComplexity', 'LawOfDemeter', 'AvoidLiteralsInIfCondition', 'AvoidPrintStackTrace', 'RedundantFieldInitializer', 'SingularField', 'ConstructorCallsOverridableMethod', 'DataClass', 'AvoidFieldNameMatchingMethodName', 'SimplifiedTernary', 'UseVarargs', 'ArrayIsStoredDirectly', 'UseCollectionIsEmpty', 'CognitiveComplexity', 'AvoidDeeplyNestedIfStmts', 'ImplicitSwitchFallThrough', 'LooseCoupling', 'CloseResource', 'AssignmentInOperand', 'SimplifyBooleanReturns', 'ExcessiveImports', 'CompareObjectsWithEquals', 'UseUtilityClass', 'EmptyCatchBlock', 'SuspiciousEqualsMethodName', 'OverrideBothEqualsAndHashcode', 'AvoidThrowingNewInstanceOfSameException', 'ConstantsInInterface', 'MoreThanOneLogger', 'ExcessivePublicCount', 'NPathComplexity', 'UnusedFormalParameter', 'AvoidCatchingThrowable', 'AvoidReassigningParameters', 'InvalidLogMessageFormat', 'OneDeclarationPerLine', 'TooFewBranchesForASwitchStatement', 'ClassWithOnlyPrivateConstructorsShouldBeFinal', 'ExcessiveParameterList', 'OptimizableToArrayCall', 'TooManyFields', 'SignatureDeclareThrowsException', 'ReturnEmptyCollectionRatherThanNull', 'NcssCount', 'SwitchStmtsShouldHaveDefault', 'StringToString', 'SystemPrintln', 'SwitchDensity', 'UnusedPrivateField', 'DoNotUseThreads', 'SimplifyBooleanExpressions', 'AddEmptyString', 'AvoidUsingHardCodedIP', 'UseTryWithResources', 'AvoidFileStream', 'DoNotThrowExceptionInFinally', 'AssignmentToNonFinalStatic', 'MethodReturnsInternalArray', 'InefficientEmptyStringCheck', 'UnusedLocalVariable', 'UseProperClassLoader', 'PrimitiveWrapperInstantiation', 'AvoidSynchronizedAtMethodLevel', 'NonSerializableClass', 'AvoidFieldNameMatchingTypeName', 'UnnecessaryCaseChange', 'UnusedPrivateMethod', 'UseEqualsToCompareStrings', 'InefficientStringBuffering', 'TestClassWithoutTestCases', 'StringInstantiation', 'ForLoopCanBeForeach', 'AbstractClassWithoutAnyMethod', 'AvoidUncheckedExceptionsInSignatures', 'DoNotTerminateVM', 'UseObjectForClearerAPI', 'AvoidStringBufferField', 'DontImportSun', 'AvoidUsingVolatile', 'DoubleBraceInitialization', 'AvoidReassigningLoopVariables', 'UseIndexOfChar', 'ReplaceVectorWithList', 'MissingSerialVersionUID', 'FinalFieldCouldBeStatic', 'FinalizeDoesNotCallSuperFinalize', 'LogicInversion', 'AvoidInstanceofChecksInCatchClause', 'CloneMethodReturnTypeMustMatchClassName', 'CloneMethodMustImplementCloneable', 'AvoidArrayLoops', 'AvoidRethrowingException', 'SimplifyConditional', 'ForLoopVariableCount', 'WhileLoopWithLiteralBoolean', 'SingletonClassReturningNewInstance', 'UselessStringValueOf', 'AvoidThreadGroup', 'UseStringBufferForStringAppends', 'AvoidBranchingStatementAsLastInLoop', 'SimpleDateFormatNeedsLocale', 'ReplaceHashtableWithMap', 'NonThreadSafeSingleton', 'AvoidUsingOctalValues', 'UseArraysAsList', 'ProperCloneImplementation', 'CloneMethodMustBePublic', 'SingleMethodSingleton', 'MissingStaticMethodInNonInstantiatableClass', 'AvoidReassigningCatchVariables', 'AvoidThrowingNullPointerException', 'UseStandardCharsets', 'UnconditionalIfStatement', 'UseArrayListInsteadOfVector', 'UselessOverridingMethod', 'AvoidMessageDigestField', 'DoNotExtendJavaLangError', 'DefaultLabelNotLastInSwitchStmt', 'AvoidCalendarDateCreation', 'CheckSkipResult', 'JUnit4TestShouldUseTestAnnotation', 'DetachedTestCase', 'JUnitTestContainsTooManyAsserts', 'UnusedNullCheckInEquals', 'NonStaticInitializer', 'UnsynchronizedStaticFormatter', 'DoNotCallGarbageCollectionExplicitly', 'AvoidDecimalLiteralsInBigDecimalConstructor', 'UseNotifyAllInsteadOfNotify', 'UselessOperationOnImmutable', 'DontCallThreadRun', 'AvoidCatchingNPE', 'BrokenNullCheck', 'ComparisonWithNaN', 'SuspiciousOctalEscape', 'MisplacedNullCheck', 'DoubleCheckedLocking', 'EqualsNull', 'UseStringBufferLength', 'UnnecessaryConversionTemporary', 'ReturnFromFinallyBlock', 'BigIntegerInstantiation', 'AvoidLosingExceptionInformation', 'JumbledIncrementer', 'AvoidMultipleUnaryOperators', 'MethodWithSameNameAsEnclosingClass', 'HardCodedCryptoKey', 'ProperLogger', 'FinalizeOverloaded', 'CheckResultSet', 'UseIOStreamsWithApacheCommonsFileItem', 'IdempotentOperations', 'InsecureCryptoIv', 'DoNotHardCodeSDCard', 'DoNotExtendJavaLangThrowable', 'JUnit5TestShouldBePackagePrivate', 'ReplaceEnumerationWithIterator', 'JUnitTestsShouldIncludeAssert', 'JUnitUseExpected', 'NonCaseLabelInSwitchStatement', 'FinalizeShouldBeProtected', 'SimplifiableTestAssertion', 'JUnitAssertionsShouldIncludeMessage', 'InstantiationToGetClass', 'Rule', 'JUnit4SuitesShouldUseSuiteAnnotation', 'JUnit4TestShouldUseBeforeAnnotation', 'UnnecessaryBooleanAssertion', 'JUnit4TestShouldUseAfterAnnotation', 'StringBufferInstantiationWithChar', 'EmptyFinalizer', 'FinalizeOnlyCallsSuperFinalize']

sonarqube_category_list = ['CODE_SMELL', 'VULNERABILITY', 'BUG']

findbugs_category_list = ['B', 'C', 'D', 'E', 'I', 'M', 'V', 'S', 'P', 'X']

findbugs_vtype_list = ['HE_HASHCODE_USE_OBJECT_EQUALS', 'EI_EXPOSE_REP2', 'EI_EXPOSE_REP', 'NP_PARAMETER_MUST_BE_NONNULL_BUT_MARKED_AS_NULLABLE',
              'NP_NULL_ON_SOME_PATH_FROM_RETURN_VALUE', 'OS_OPEN_STREAM', 'REFLC_REFLECTION_MAY_INCREASE_ACCESSIBILITY_OF_CLASS',
              'DP_DO_INSIDE_DO_PRIVILEGED', 'DM_CONVERT_CASE', 'REC_CATCH_EXCEPTION', 'THROWS_METHOD_THROWS_RUNTIMEEXCEPTION',
              'DB_DUPLICATE_SWITCH_CLAUSES', 'BC_BAD_CAST_TO_ABSTRACT_COLLECTION', 'BC_IMPOSSIBLE_DOWNCAST_OF_TOARRAY',
              'RCN_REDUNDANT_NULLCHECK_WOULD_HAVE_BEEN_A_NPE', 'SF_SWITCH_NO_DEFAULT', 'DB_DUPLICATE_BRANCHES', 'THROWS_METHOD_THROWS_CLAUSE_THROWABLE',
              'NP_NULL_ON_SOME_PATH', 'MC_OVERRIDABLE_METHOD_CALL_IN_CONSTRUCTOR', 'SIC_INNER_SHOULD_BE_STATIC_ANON',
              'UWF_FIELD_NOT_INITIALIZED_IN_CONSTRUCTOR', 'MS_SHOULD_BE_FINAL', 'SE_COMPARATOR_SHOULD_BE_SERIALIZABLE',
              'UCF_USELESS_CONTROL_FLOW', 'NP_LOAD_OF_KNOWN_NULL_VALUE', 'THROWS_METHOD_THROWS_CLAUSE_BASIC_EXCEPTION',
              'URF_UNREAD_PUBLIC_OR_PROTECTED_FIELD', 'MS_PKGPROTECT', 'DMI_INVOKING_TOSTRING_ON_ARRAY', 'UUF_UNUSED_PUBLIC_OR_PROTECTED_FIELD',
              'MF_CLASS_MASKS_FIELD', 'DM_STRING_TOSTRING', 'ST_WRITE_TO_STATIC_FROM_INSTANCE_METHOD', 'NP_NULL_PARAM_DEREF_NONVIRTUAL',
              'DLS_DEAD_LOCAL_STORE', 'MS_EXPOSE_REP', 'RV_RETURN_VALUE_IGNORED_BAD_PRACTICE', 'DM_DEFAULT_ENCODING', 'RV_RETURN_VALUE_IGNORED',
              'WMI_WRONG_MAP_ITERATOR', 'NM_CONFUSING', 'IS2_INCONSISTENT_SYNC', 'PZLA_PREFER_ZERO_LENGTH_ARRAYS', 'DMI_RANDOM_USED_ONLY_ONCE',
              'DM_NUMBER_CTOR', 'DMI_ENTRY_SETS_MAY_REUSE_ENTRY_OBJECTS', 'URF_UNREAD_FIELD', 'SE_BAD_FIELD', 'EQ_UNUSUAL',
              'EQ_CHECK_FOR_OPERAND_NOT_COMPATIBLE_WITH_THIS', 'EQ_OVERRIDING_EQUALS_NOT_SYMMETRIC', 'FE_FLOATING_POINT_EQUALITY',
              'CN_IDIOM_NO_SUPER_CALL', 'SE_PRIVATE_READ_RESOLVE_NOT_INHERITED', 'RI_REDUNDANT_INTERFACES', 'DP_CREATE_CLASSLOADER_INSIDE_DO_PRIVILEGED',
              'SBSC_USE_STRINGBUFFER_CONCATENATION', 'CO_COMPARETO_INCORRECT_FLOATING', 'BC_UNCONFIRMED_CAST', 'SE_NO_SERIALVERSIONID',
              'HE_INHERITS_EQUALS_USE_HASHCODE', 'CI_CONFUSED_INHERITANCE', 'CO_ABSTRACT_SELF', 'NP_METHOD_PARAMETER_TIGHTENS_ANNOTATION',
              'NP_BOOLEAN_RETURN_NULL', 'UPM_UNCALLED_PRIVATE_METHOD', 'RV_NEGATING_RESULT_OF_COMPARETO', 'UC_USELESS_VOID_METHOD',
              'BC_EQUALS_METHOD_SHOULD_WORK_FOR_ALL_OBJECTS', 'HE_EQUALS_USE_HASHCODE', 'FL_FLOATS_AS_LOOP_COUNTERS', 'EQ_COMPARETO_USE_OBJECT_EQUALS',
              'NP_TOSTRING_COULD_RETURN_NULL', 'RR_NOT_CHECKED', 'RCN_REDUNDANT_NULLCHECK_OF_NONNULL_VALUE', 'OBL_UNSATISFIED_OBLIGATION',
              'SE_BAD_FIELD_INNER_CLASS', 'DLS_DEAD_LOCAL_STORE_OF_NULL', 'DM_FP_NUMBER_CTOR', 'DM_EXIT', 'WA_AWAIT_NOT_IN_LOOP',
              'SF_SWITCH_FALLTHROUGH', 'SE_TRANSIENT_FIELD_NOT_RESTORED', 'DM_BOXED_PRIMITIVE_FOR_COMPARE', 'SE_INNER_CLASS', 'VO_VOLATILE_INCREMENT',
              'INT_BAD_COMPARISON_WITH_NONNEGATIVE_VALUE', 'INT_BAD_COMPARISON_WITH_SIGNED_BYTE', 'NM_SAME_SIMPLE_NAME_AS_SUPERCLASS',
              'ES_COMPARING_STRINGS_WITH_EQ', 'DE_MIGHT_IGNORE', 'STCAL_STATIC_SIMPLE_DATE_FORMAT_INSTANCE', 'NP_EQUALS_SHOULD_HANDLE_NULL_ARGUMENT',
              'BC_UNCONFIRMED_CAST_OF_RETURN_VALUE', 'EQ_DOESNT_OVERRIDE_EQUALS', 'SIO_SUPERFLUOUS_INSTANCEOF', 'ICAST_QUESTIONABLE_UNSIGNED_RIGHT_SHIFT',
              'ME_MUTABLE_ENUM_FIELD', 'UC_USELESS_OBJECT', 'IT_NO_SUCH_ELEMENT', 'NO_NOTIFY_NOT_NOTIFYALL', 'DM_BOXED_PRIMITIVE_FOR_PARSING',
              'CNT_ROUGH_CONSTANT_VALUE', 'DMI_NONSERIALIZABLE_OBJECT_WRITTEN', 'OBL_UNSATISFIED_OBLIGATION_EXCEPTION_EDGE', 'DMI_COLLECTION_OF_URLS',
              'NM_CLASS_NAMING_CONVENTION', 'JLM_JSR166_UTILCONCURRENT_MONITORENTER', 'NP_NULL_ON_SOME_PATH_EXCEPTION', 'EI_EXPOSE_STATIC_REP2',
              'ICAST_INTEGER_MULTIPLY_CAST_TO_LONG', 'UMAC_UNCALLABLE_METHOD_OF_ANONYMOUS_CLASS', 'SA_LOCAL_SELF_COMPARISON', 'IL_INFINITE_RECURSIVE_LOOP',
              'UC_USELESS_CONDITION', 'SA_FIELD_SELF_ASSIGNMENT', 'DCN_NULLPOINTER_EXCEPTION', 'RV_RETURN_VALUE_IGNORED_NO_SIDE_EFFECT', 'CN_IDIOM',
              'NM_SAME_SIMPLE_NAME_AS_INTERFACE', 'VA_FORMAT_STRING_USES_NEWLINE', 'NS_NON_SHORT_CIRCUIT', 'NM_FIELD_NAMING_CONVENTION',
              'RV_CHECK_FOR_POSITIVE_INDEXOF', 'RV_CHECK_COMPARETO_FOR_SPECIFIC_RETURN_VALUE', 'BC_VACUOUS_INSTANCEOF', 'DM_NEW_FOR_GETCLASS',
              'ICAST_BAD_SHIFT_AMOUNT', 'RC_REF_COMPARISON_BAD_PRACTICE_BOOLEAN', 'ISC_INSTANTIATE_STATIC_CLASS', 'NN_NAKED_NOTIFY',
              'OS_OPEN_STREAM_EXCEPTION_PATH', 'SE_NO_SUITABLE_CONSTRUCTOR', 'ES_COMPARING_PARAMETER_STRING_WITH_EQ',
              'HE_HASHCODE_NO_EQUALS', 'INT_VACUOUS_BIT_OPERATION', 'LI_LAZY_INIT_STATIC', 'SC_START_IN_CTOR',
              'RpC_REPEATED_CONDITIONAL_TEST', 'DMI_HARDCODED_ABSOLUTE_FILENAME', 'MC_OVERRIDABLE_METHOD_CALL_IN_CLONE', 'INT_BAD_REM_BY_1',
              'EQ_SELF_NO_OBJECT', 'CO_SELF_NO_OBJECT', 'IM_BAD_CHECK_FOR_ODD', 'DM_STRING_CTOR', 'INT_VACUOUS_COMPARISON',
              'UR_UNINIT_READ_CALLED_FROM_SUPER_CONSTRUCTOR', 'DM_BOOLEAN_CTOR', 'SF_DEAD_STORE_DUE_TO_SWITCH_FALLTHROUGH',
              'RCN_REDUNDANT_NULLCHECK_OF_NULL_VALUE', 'NP_NULL_PARAM_DEREF', 'IL_INFINITE_LOOP', 'IP_PARAMETER_IS_DEAD_BUT_OVERWRITTEN',
              'NS_DANGEROUS_NON_SHORT_CIRCUIT', 'REFLF_REFLECTION_MAY_INCREASE_ACCESSIBILITY_OF_FIELD',
              'IA_AMBIGUOUS_INVOCATION_OF_INHERITED_OR_OUTER_METHOD', 'IC_SUPERCLASS_USES_SUBCLASS_DURING_INITIALIZATION',
              'UR_UNINIT_READ', 'HE_EQUALS_NO_HASHCODE', 'CN_IMPLEMENTS_CLONE_BUT_NOT_CLONEABLE', 'BC_IMPOSSIBLE_CAST',
              'STCAL_INVOKE_ON_STATIC_DATE_FORMAT_INSTANCE', 'NP_CLONE_COULD_RETURN_NULL', 'EC_UNRELATED_TYPES_USING_POINTER_EQUALITY',
              'IM_AVERAGE_COMPUTATION_COULD_OVERFLOW', 'RV_RETURN_VALUE_OF_PUTIFABSENT_IGNORED', 'SA_LOCAL_DOUBLE_ASSIGNMENT',
              'RS_READOBJECT_SYNC', 'UG_SYNC_SET_UNSYNC_GET', 'RC_REF_COMPARISON_BAD_PRACTICE', 'ICAST_INT_CAST_TO_DOUBLE_PASSED_TO_CEIL',
              'EC_UNRELATED_TYPES', 'ICAST_IDIV_CAST_TO_DOUBLE', 'PZ_DONT_REUSE_ENTRY_OBJECTS_IN_ITERATORS', 'BC_IMPOSSIBLE_INSTANCEOF',
              'NP_NONNULL_PARAM_VIOLATION', 'SA_FIELD_DOUBLE_ASSIGNMENT', 'BX_UNBOXING_IMMEDIATELY_REBOXED', 'LI_LAZY_INIT_UPDATE_STATIC',
              'DM_NEXTINT_VIA_NEXTDOUBLE', 'UL_UNRELEASED_LOCK', 'UI_INHERITANCE_UNSAFE_GETRESOURCE', 'NP_GUARANTEED_DEREF',
              'DLS_DEAD_LOCAL_STORE_SHADOWS_FIELD', 'RCN_REDUNDANT_COMPARISON_OF_NULL_AND_NONNULL_VALUE', 'NP_NULL_PARAM_DEREF_ALL_TARGETS_DANGEROUS',
              'NM_METHOD_NAMING_CONVENTION', 'WA_NOT_IN_LOOP', 'UWF_UNWRITTEN_PUBLIC_OR_PROTECTED_FIELD', 'UWF_UNWRITTEN_FIELD', 'UWF_NULL_FIELD',
              'UUF_UNUSED_FIELD', 'SIC_INNER_SHOULD_BE_STATIC', 'SIC_THREADLOCAL_DEADLY_EMBRACE', 'SIC_INNER_SHOULD_BE_STATIC_NEEDS_THIS',
              'SS_SHOULD_BE_STATIC', 'NP_UNWRITTEN_FIELD', 'VO_VOLATILE_REFERENCE_TO_ARRAY', 'HE_USE_OF_UNHASHABLE_CLASS', 'MS_OOI_PKGPROTECT',
              'MS_MUTABLE_COLLECTION_PKGPROTECT', 'MS_CANNOT_BE_FINAL', 'MS_MUTABLE_ARRAY', 'MS_SHOULD_BE_REFACTORED_TO_BE_FINAL', 'MS_FINAL_PKGPROTECT',
              'MS_MUTABLE_COLLECTION', 'DM_STRING_VOID_CTOR', 'EQ_ABSTRACT_SELF', 'ESync_EMPTY_SYNC', 'DM_MONITOR_WAIT_ON_CONDITION', 'EQ_SELF_USE_OBJECT',
              'BSHIFT_WRONG_ADD_PRIORITY', 'NM_CLASS_NOT_EXCEPTION', 'SE_BAD_FIELD_STORE', 'FI_PUBLIC_SHOULD_BE_PROTECTED',
              'BC_BAD_CAST_TO_CONCRETE_COLLECTION', 'NP_NULL_ON_SOME_PATH_MIGHT_BE_INFEASIBLE', 'AT_OPERATION_SEQUENCE_ON_CONCURRENT_ABSTRACTION',
              'DM_BOXED_PRIMITIVE_TOSTRING', 'SQL_NONCONSTANT_STRING_PASSED_TO_EXECUTE', 'FI_MISSING_SUPER_CALL', 'UCF_USELESS_CONTROL_FLOW_NEXT_LINE',
              'NP_DEREFERENCE_OF_READLINE_VALUE', 'NP_UNWRITTEN_PUBLIC_OR_PROTECTED_FIELD', 'IC_INIT_CIRCULARITY',
              'SQL_PREPARED_STATEMENT_GENERATED_FROM_NONCONSTANT_STRING', 'IS_FIELD_NOT_GUARDED', 'VA_PRIMITIVE_ARRAY_PASSED_TO_OBJECT_VARARG',
              'DMI_INVOKING_HASHCODE_ON_ARRAY', 'BIT_IOR_OF_SIGNED_BYTE', 'EC_BAD_ARRAY_COMPARE', 'UC_USELESS_CONDITION_TYPE', 'BIT_SIGNED_CHECK',
              'RC_REF_COMPARISON', 'SA_LOCAL_SELF_COMPUTATION', 'SKIPPED_CLASS_TOO_BIG', 'UW_UNCOND_WAIT', 'DM_GC', 'ME_ENUM_FIELD_SETTER',
              'DMI_USING_REMOVEALL_TO_CLEAR_COLLECTION', 'SWL_SLEEP_WITH_LOCK_HELD', 'NP_ALWAYS_NULL', 'UM_UNNECESSARY_MATH',
              'JUA_DONT_ASSERT_INSTANCEOF_IN_TESTS', 'MTIA_SUSPECT_SERVLET_INSTANCE_FIELD', 'DC_DOUBLECHECK', 'GC_UNRELATED_TYPES',
              'MSF_MUTABLE_SERVLET_FIELD', 'NM_VERY_CONFUSING', 'ML_SYNC_ON_FIELD_TO_GUARD_CHANGING_THAT_FIELD', 'SE_METHOD_MUST_BE_PRIVATE',
              'TQ_NEVER_VALUE_USED_WHERE_ALWAYS_REQUIRED', 'RV_RETURN_VALUE_IGNORED_INFERRED', 'SW_SWING_METHODS_INVOKED_IN_SWING_THREAD',
              'DL_SYNCHRONIZATION_ON_BOXED_PRIMITIVE', 'DMI_BLOCKING_METHODS_ON_URL', 'SI_INSTANCE_BEFORE_FINALS_ASSIGNED',
              'BX_BOXING_IMMEDIATELY_UNBOXED_TO_PERFORM_COERCION', 'RV_EXCEPTION_NOT_THROWN', 'DMI_USELESS_SUBSTRING', 'SR_NOT_CHECKED',
              'UL_UNRELEASED_LOCK_EXCEPTION_PATH', 'RV_ABSOLUTE_VALUE_OF_RANDOM_INT', 'SSD_DO_NOT_USE_INSTANCE_LOCK_ON_SHARED_STATIC_DATA',
              'SA_FIELD_SELF_COMPARISON', 'NP_IMMEDIATE_DEREFERENCE_OF_READLINE', 'HSC_HUGE_SHARED_STRING_CONSTANT', 'EQ_COMPARING_CLASS_NAMES',
              'EC_UNRELATED_CLASS_AND_INTERFACE', 'SA_FIELD_SELF_COMPUTATION', 'INT_BAD_COMPARISON_WITH_INT_VALUE', 'ML_SYNC_ON_UPDATED_FIELD',
              'ODR_OPEN_DATABASE_RESOURCE_EXCEPTION_PATH', 'ODR_OPEN_DATABASE_RESOURCE', 'NP_NONNULL_FIELD_NOT_INITIALIZED_IN_CONSTRUCTOR',
              'LG_LOST_LOGGER_DUE_TO_WEAK_REFERENCE', 'RANGE_ARRAY_INDEX', 'NP_NONNULL_RETURN_VIOLATION', 'SQL_BAD_RESULTSET_ACCESS', 'NM_WRONG_PACKAGE',
              'EQ_ALWAYS_FALSE', 'EC_NULL_ARG', 'NP_GUARANTEED_DEREF_ON_EXCEPTION_PATH', 'IJU_ASSERT_METHOD_INVOKED_FROM_RUN_METHOD',
              'EQ_GETCLASS_AND_CLASS_CONSTANT', 'EC_ARRAY_AND_NONARRAY', 'FI_FINALIZER_NULLS_FIELDS', 'SA_LOCAL_SELF_ASSIGNMENT',
              'DL_SYNCHRONIZATION_ON_UNSHARED_BOXED_PRIMITIVE', 'NM_LCASE_HASHCODE', 'RE_POSSIBLE_UNINTENDED_PATTERN', 'FI_NULLIFY_SUPER',
              'IM_MULTIPLYING_RESULT_OF_IREM', 'FI_EMPTY', 'QBA_QUESTIONABLE_BOOLEAN_ASSIGNMENT', 'DL_SYNCHRONIZATION_ON_SHARED_CONSTANT',
              'MWN_MISMATCHED_NOTIFY', 'RU_INVOKE_RUN', 'HRS_REQUEST_PARAMETER_TO_HTTP_HEADER', 'STCAL_INVOKE_ON_STATIC_CALENDAR_INSTANCE',
              'NM_FUTURE_KEYWORD_USED_AS_MEMBER_IDENTIFIER', 'NM_FUTURE_KEYWORD_USED_AS_IDENTIFIER', 'BIT_AND', 'DLS_DEAD_STORE_OF_CLASS_LITERAL',
              'SE_NO_SUITABLE_CONSTRUCTOR_FOR_EXTERNALIZATION', 'BIT_IOR', 'CO_COMPARETO_RESULTS_MIN_VALUE', 'DLS_DEAD_LOCAL_STORE_IN_RETURN',
              'JCIP_FIELD_ISNT_FINAL_IN_IMMUTABLE_CLASS', 'PERM_SUPER_NOT_CALLED_IN_GETPERMISSIONS', 'WS_WRITEOBJECT_SYNC',
              'RV_DONT_JUST_NULL_CHECK_READLINE', 'BX_BOXING_IMMEDIATELY_UNBOXED', 'UC_USELESS_OBJECT_STACK', 'QF_QUESTIONABLE_FOR_LOOP',
              'BIT_AND_ZZ', 'ICAST_INT_2_LONG_AS_INSTANT', 'SA_LOCAL_SELF_ASSIGNMENT_INSTEAD_OF_FIELD', 'DC_PARTIALLY_CONSTRUCTED',
              'IMSE_DONT_CATCH_IMSE', 'DMI_CONSTANT_DB_PASSWORD', 'XSS_REQUEST_PARAMETER_TO_SERVLET_WRITER', 'NP_METHOD_RETURN_RELAXING_ANNOTATION',
              'DMI_EMPTY_DB_PASSWORD', 'EQ_ALWAYS_TRUE', 'DMI_INVOKING_TOSTRING_ON_ANONYMOUS_ARRAY', 'EI_EXPOSE_BUF',
              'DMI_BIGDECIMAL_CONSTRUCTED_FROM_DOUBLE', 'J2EE_STORE_OF_NON_SERIALIZABLE_OBJECT_INTO_SESSION', 'XSS_REQUEST_PARAMETER_TO_SEND_ERROR',
              'MTIA_SUSPECT_STRUTS_INSTANCE_FIELD', 'NM_METHOD_CONSTRUCTOR_CONFUSION', 'NM_BAD_EQUAL', 'RCN_REDUNDANT_COMPARISON_TWO_NULL_VALUES',
              'STI_INTERRUPTED_ON_CURRENTTHREAD', 'STCAL_STATIC_CALENDAR_INSTANCE', 'NP_ALWAYS_NULL_EXCEPTION', 'SP_SPIN_ON_FIELD',
              'SF_DEAD_STORE_DUE_TO_SWITCH_FALLTHROUGH_TO_THROW', 'BX_UNBOXED_AND_COERCED_FOR_TERNARY_OPERATOR',
              'WL_USING_GETCLASS_RATHER_THAN_CLASS_LITERAL', 'SE_NONLONG_SERIALVERSIONID', 'DMI_VACUOUS_SELF_COLLECTION_CALL', 'DM_INVALID_MIN_MAX',
              'EI_EXPOSE_BUF2', 'HE_SIGNATURE_DECLARES_HASHING_OF_UNHASHABLE_CLASS', 'RV_ABSOLUTE_VALUE_OF_HASHCODE', 'NP_NULL_INSTANCEOF',
              'TLW_TWO_LOCK_WAIT', 'MWN_MISMATCHED_WAIT', 'NM_VERY_CONFUSING_INTENTIONAL', 'ICAST_INT_CAST_TO_FLOAT_PASSED_TO_ROUND',
              'FI_EXPLICIT_INVOCATION', 'DMI_DOH', 'DM_USELESS_THREAD', 'RANGE_ARRAY_OFFSET', 'MS_MUTABLE_HASHTABLE', 'NP_STORE_INTO_NONNULL_FIELD',
              'XFB_XML_FACTORY_BYPASS', 'RV_REM_OF_HASHCODE', 'DMI_CALLING_NEXT_FROM_HASNEXT', 'FE_TEST_IF_EQUAL_TO_NOT_A_NUMBER',
              'NM_WRONG_PACKAGE_INTENTIONAL', 'NP_CLOSING_NULL', 'TESTING', 'FI_USELESS', 'BIT_SIGNED_CHECK_HIGH_BIT', 'JLM_JSR166_LOCK_MONITORENTER',
              'RE_BAD_SYNTAX_FOR_REGULAR_EXPRESSION', 'RV_01_TO_INT', 'EC_UNRELATED_INTERFACES', 'BIT_ADD_OF_SIGNED_BYTE',
              'XSS_REQUEST_PARAMETER_TO_JSP_WRITER', 'DL_SYNCHRONIZATION_ON_BOOLEAN', 'DMI_THREAD_PASSED_WHERE_RUNNABLE_EXPECTED',
              'RANGE_STRING_INDEX', 'IJU_NO_TESTS', 'DM_RUN_FINALIZERS_ON_EXIT', 'PT_ABSOLUTE_PATH_TRAVERSAL', 'PT_RELATIVE_PATH_TRAVERSAL',
              'RANGE_ARRAY_LENGTH', 'IJU_TEARDOWN_NO_SUPER', 'DMI_COLLECTIONS_SHOULD_NOT_CONTAIN_THEMSELVES']



metrics_types = ['Annotation', 'Type', 'TypeVariable', 'Constructor', 'Method', 'Class', 'Interface', 'File', 'Package']
start_loc = fileMap.get("resolution_line") + 1

selected_features = [18, 44, 45, 46, 47, 48, 49, 53, 54, 55, 56, 57, 58, 59, 63, 65, 66, 67, 68, 71, 72, 74, 75, 86, 87, 88, 89, 92, 93, 95, 98, 100, 103, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 119, 121, 122, 123, 124, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 141, 142, 143, 144, 145, 146, 148, 150, 151, 152, 153, 154, 155, 156, 158, 159, 160, 161, 162, 163, 164, 165, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 191, 192, 193, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 215, 216, 217, 218, 219, 220, 221, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 249, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 293, 294, 295, 297, 298, 299, 300, 301]

print(len(selected_features))